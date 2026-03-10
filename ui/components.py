import streamlit as st
import json
from database.neo4j_ops import Neo4jManager
from logger import get_logger

db = Neo4jManager()
logger = get_logger("components")

@st.dialog("Clear All History")
def confirm_clear_all():
    st.write("Are you sure you want to delete all the lessons you created?")
    col1, col2 = st.columns(2)
    if col1.button("Yes, delete", use_container_width=True, type="primary"):
        db.clear_all()
        st.session_state.page = "generate"
        st.rerun()
    if col2.button("No, keep them", use_container_width=True):
        st.rerun()

@st.dialog("Clear Course")
def confirm_clear_course(course_title):
    st.write(f"Are you sure you want to delete **{course_title}**?")
    st.warning("This action cannot be undone.")
    
    col1, col2 = st.columns(2)
    
    if col1.button("Yes, delete", use_container_width=True, type="primary"):
        db.delete_course(course_title)
        # Rerun here is GOOD because it refreshes the sidebar list 
        # after the database change.
        st.rerun() 
        
    if col2.button("No, keep it", use_container_width=True):
        # In a dialog, doing nothing or calling st.rerun() 
        # will effectively close the dialog.
        st.rerun()

def render_sidebars():
    with st.sidebar:
        if st.session_state.page == "view":
            # --- VIEW MODE SIDEBAR: ROADMAP & SCOREBOARD ---
            if st.button("⬅️ New Course", use_container_width=True, type="primary"):
                st.session_state.page = "generate"
                st.session_state.score = 0
                st.session_state.answered_questions = set()
                st.rerun()
            
            st.markdown("---")
            
            # --- NEW: SCOREBOARD SECTION ---
            st.subheader("🏆 Your Progress")
            data = db.get_course_by_title(st.session_state.current_course_title)
            if data:
                course_json = json.loads(data['content']) if isinstance(data['content'], str) else data['content']
    
                # Calculate Total Questions
                total_q = sum(len(m.get('module_quiz', [])) for m in course_json.get('modules', []))
                
                # Safely get submitted quizzes
                submitted = st.session_state.get('submitted_quizzes', {})
                
                # Correct Answers
                current_s = st.session_state.get('score', 0)
                
                # Calculate Answered Questions
                total_answered = sum(len(results) for results in submitted.values())
                
                # Calculate Progress %
                # We ensure total_q > 0 to avoid division by zero
                progress = (total_answered / total_q) if total_q > 0 else 0
                
                col1, col2 = st.columns(2)
                col1.metric("Correct", f"{current_s}/{total_q}")
                col2.metric("Progress", f"{int(progress * 100)}%")
                st.progress(progress)
            
            st.markdown("---")
            
            # --- ROADMAP SECTION ---
            st.subheader("🗺️ Course Roadmap")
            structure = db.get_course_structure(st.session_state.current_course_title)
            for row in structure:
                mod_title = row['module']
                mod_id = mod_title.lower().replace(" ", "-")
                
                # Check if this specific module ID exists in our submitted_quizzes dict
                is_done = mod_id in st.session_state.get('submitted_quizzes', {})
                icon = "✅" if is_done else "📖"
                
                st.markdown(f'<a href="#{mod_id}" target="_self" class="roadmap-link roadmap-module">{icon} {mod_title}</a>', unsafe_allow_html=True)
                for lesson in row['lessons']:
                    st.markdown(f'<a href="#{lesson.lower().replace(" ", "-")}" target="_self" class="roadmap-link">&nbsp;&nbsp;&nbsp;&nbsp;• {lesson}</a>', unsafe_allow_html=True)
        else:
            # --- GENERATE MODE SIDEBAR: HISTORY ONLY ---
            st.subheader("📚 Course History")
            st.markdown("---")
            history = db.get_history()
            if history:
                for item in history:
                    with st.container():
                        st.markdown(f"**{item['title']}**")
                        st.caption(f"{item['diff']} | Duration: {item['h']} Hours")
                        c1, c2 = st.columns([3,1])
                        if c1.button("👀 View", key=f"v_{item['title']}", use_container_width=True):
                            # 1. Update the target course
                            st.session_state.current_course_title = item['title']
                            st.session_state.page = "view"
                            
                            # 2. CLEAR previous session quiz data so the new course starts fresh
                            st.session_state.score = 0
                            st.session_state.submitted_quizzes = {}
                            
                            st.rerun()
                        if c2.button("🗑️", key=f"d_{item['title']}", use_container_width=True):
                            confirm_clear_course(item['title'])
            else:
                st.info("No courses created yet. Start by generating a new course on the main page!")
                        
            st.markdown("---")
            if st.button("Clear All", use_container_width=True, icon="🚨", type="primary"):
                confirm_clear_all()

def render_course_view():
    data = db.get_course_by_title(st.session_state.current_course_title)
    if not data:
        st.error("Course not found.")
        return

    # Initialize Session States
    if "score" not in st.session_state: st.session_state.score = 0
    if "submitted_quizzes" not in st.session_state: st.session_state.submitted_quizzes = {} # {mod_id: {q_idx: is_correct}}

    display_title = data.get('gen_title') or data['title']
    st.title(display_title)
    st.caption(f"Duration: {data['h']} Hours | Expertise: {data['diff']} ")
    st.markdown("---")

    course_json = json.loads(data['content']) if isinstance(data['content'], str) else data['content']

    for module in course_json.get('modules', []):
        mod_title = module.get('module_title')
        mod_id = mod_title.lower().replace(" ", "-")
        st.header(mod_title, anchor=mod_id)
        
        # Inside your loop in render_course_view (ui/components.py)
        for lesson in module.get('lessons', []):
            st.subheader(lesson.get('lesson_title'))
            
            # Show the duration and summary as a nice caption
            st.caption(f"⏱️ Duration: {lesson.get('duration_hours')} hrs | 🎯 Objective: {lesson.get('learning_objective')}")
            st.write(f"*{lesson.get('brief_summary')}*")

            # Create Tabs for different content types
            tab1, tab2 = st.tabs(["📖 Reading Material", "🎥 Video Script"])
            
            with tab1:
                st.markdown(lesson.get('explanation_markdown') or lesson.get('content'))
                
            with tab2:
                st.info("💡 This script is designed for a short educational video accompaniment.")
                st.text_area("Video Script", lesson.get('video_script'), height=300, disabled=True)
       
        # --- MODULE QUIZ FORM ---
        quiz_data = module.get('module_quiz', [])
        if quiz_data:
            with st.expander(f"📝 Module Exam: {mod_title}", expanded=False):
                # If already submitted, show the results directly
                if mod_id in st.session_state.submitted_quizzes:
                    results = st.session_state.submitted_quizzes[mod_id]
                    correct_count = sum(1 for r in results.values() if r["is_correct"])
                    st.info(f"Exam Completed. Your Score: {correct_count}/{len(quiz_data)}")
                    
                    for idx, q in enumerate(quiz_data):
                        res = results[idx]
                        st.write(f"**Q{idx+1}: {q['question']}**")
                        if res["is_correct"]:
                            st.success(f"Correct! You chose: {res['user_choice']}")
                        else:
                            st.error(f"Wrong. You chose: {res['user_choice']}. Correct Answer: {q['answer']}")
                else:
                    # Create a Form for the Quiz
                    with st.form(key=f"form_{mod_id}"):
                        user_selections = {}
                        for idx, q in enumerate(quiz_data):
                            st.write(f"**Q{idx+1}: {q['question']}**")
                            user_selections[idx] = st.radio(" ", q['options'], key=f"radio_{mod_id}_{idx}")
                        
                        submit_quiz = st.form_submit_button("Submit Exam", use_container_width=True)
                        
                        if submit_quiz:
                            module_results = {}
                            new_score_gain = 0
                            for idx, q in enumerate(quiz_data):
                                is_correct = user_selections[idx] == q['answer']
                                if is_correct: new_score_gain += 1
                                module_results[idx] = {
                                    "is_correct": is_correct,
                                    "user_choice": user_selections[idx]
                                }
                            
                            # Update Global State
                            st.session_state.submitted_quizzes[mod_id] = module_results
                            st.session_state.score += new_score_gain
                            st.balloons()
                            st.rerun()
        st.write("---")