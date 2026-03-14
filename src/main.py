import streamlit as st
from src.llm_factory import LlmFactory
from ui.styles import apply_custom_css
from ui.components import render_sidebars, render_course_view
from src.graph.graph import create_graph
from src.logger.logger import get_logger

logger = get_logger("MainApp")

# 1. Config
st.set_page_config(page_title="Course Architect AI", layout="centered", initial_sidebar_state="expanded")
apply_custom_css()

# 2. Session State
if "page" not in st.session_state: st.session_state.page = "generate"
if "current_course_title" not in st.session_state: st.session_state.current_course_title = ""
if "duration" not in st.session_state: st.session_state.duration = 4
if "topic_input" not in st.session_state: st.session_state.topic_input = ""
if "expertise_level" not in st.session_state: st.session_state.expertise_level = "Beginner"
if "interests_input" not in st.session_state: st.session_state.interests_input = ""
if "final_content" not in st.session_state: st.session_state.final_content = ""

# 3. LLM & Workflow
llm = LlmFactory(model="GROQ").get_llm()
app_graph = create_graph(llm)

# 4. Sidebar
# Render Sidebar (Handles History and Roadmap)
render_sidebars()

# 5. Main UI
# Router
if st.session_state.page == "view":
    render_course_view()
else:
    st.title("Start Your Learning Journey")
    st.subheader("Powered by Local Multi-Agent AI")

    with st.container(border=True, key="container"):
        topic = st.text_input("What do you want to learn? *", value=st.session_state.topic_input, placeholder="e.g., Python programming", help="Choose a topic you're interested in learning about.")
        
        col1, col2 = st.columns(2, vertical_alignment="bottom")
        with col1:
            expertise = st.selectbox("Select Expertise", options=["Beginner", "Intermediate", "Advanced"], index=["Beginner", "Intermediate", "Advanced"].index(st.session_state.expertise_level), help="Choose the level of expertise you want this course to be.")
        with col2:
            d_col1, d_col2, d_col3 = st.columns([2, 1, 1], vertical_alignment="bottom", gap="small")
            with d_col1:
                st.session_state.duration = st.number_input("Duration (Hours)", min_value=1, value=st.session_state.duration, help="How many hours can you dedicate for this course?")
            with d_col2:
                if st.button("+2", key="s1"): st.session_state.duration += 2; st.rerun()
            with d_col3:
                if st.button("+6", key="s2"): st.session_state.duration += 6; st.rerun()

        interests = st.text_area("Specific Interests", value=st.session_state.interests_input, placeholder="Focus more on this aspect, e.g. AI Agents", height=100)

        if st.button("✨ Generate Course", use_container_width=True, key="primary-btn"):
                if not topic:
                    st.error("Please enter a topic.")
                else:
                    logger.info(f"User initiated process: {topic} ({expertise})")
                    
                    with st.status("Agents are analyzing and building your course...") as status:
                        # 1. Set up inputs
                        inputs = {
                            "topic": topic, 
                            "expertise": expertise, 
                            "duration": st.session_state.duration, 
                            "interests": interests
                        }
                        
                        # 2. Run the LangGraph (Discovery -> Deconstructor -> Librarian -> Professor)
                        res = app_graph.invoke(inputs)
                        
                        # 3. Handle the output
                        # If discovery found a match, 'res' contains the existing title
                        # If it generated a new one, 'res' contains the state from the Professor
                        final_topic = res.get("topic", topic)
                        
                        if res.get("exists"):
                            status.update(label="🎯 Found a matching course in the database!", state="complete")
                            st.toast(f"Loading existing course: {final_topic}")
                        else:
                            status.update(label="✅ New course generated successfully!", state="complete")
                            st.balloons()

                    # 4. Redirect to View Page using the final identified topic
                    st.session_state.current_course_title = final_topic
                    st.session_state.page = "view"
                    
                    logger.info(f"Workflow finished for: {final_topic}")
                    st.rerun()

    # if st.session_state.final_content:
    #     st.write("---")
    #     st.markdown(st.session_state.final_content)