import json
from langchain_core.prompts import ChatPromptTemplate
from database.neo4j_ops import Neo4jManager
from .tools import search_wikipedia, search_duckduckgo, search_arxiv
from utils.helpers import load_prompt
from logger import get_logger

logger = get_logger("Librarian")
db = Neo4jManager()

def librarian_agent(state, llm):
    logger.info(f"📚 Librarian researching: {state['topic']}")
    
    # 1. Fetch the skeleton structure created by the Deconstructor
    structure = db.get_course_structure(state['topic'])
    
    # 2. Manual Tool Loop (The "Research" phase)
    # We gather raw data in Python first to avoid LLM tool-calling hallucinations
    all_raw_research = []
    for row in structure:
        module_name = row['module']
        lessons_data = []
        
        for lesson_title in row['lessons']:
            logger.info(f"🔍 Digging into: {lesson_title}")
            
            # Use your existing tools
            wiki = search_wikipedia(lesson_title)
            web = search_duckduckgo(f"{lesson_title} academic overview")
            arxiv = search_arxiv(lesson_title)
            
            combined = f"WIKI: {wiki}\nWEB: {web}\nARXIV: {arxiv}"
            lessons_data.append({
                "title": lesson_title,
                "raw_content": combined[:4000] # Cap to stay within context limits
            })
            
        all_raw_research.append({
            "module": module_name,
            "lessons": lessons_data
        })

    # 3. The "Synthesis" phase (LLM uses the .txt prompt)
    # Now we send this massive pile of raw data to the LLM to "clean it up"
    template_str = load_prompt("librarian.txt")
    prompt = ChatPromptTemplate.from_template(template_str)
    
    chain = prompt | llm
    res = chain.invoke({
        "topic": state['topic'],
        "expertise": state['expertise'],
        "structure": str(all_raw_research) # Pass the raw data here
    })

    # 4. Final Processing
    data = json.loads(res.content.replace("```json", "").replace("```", "").strip())

    for module in data['research_data']:
        for lesson in module['lessons']:
            db.graph.query("""
                MATCH (c:Course)-[:HAS_MODULE]->(m:Module {title: $m_t})
                MATCH (m)-[:HAS_LESSON]->(l:Lesson {title: $l_t})
                WHERE c.title = $c_t OR c.generated_title = $c_t
                SET l.info = $info
            """, params={
                "c_t": state['topic'],
                "m_t": module['module_title'],
                "l_t": lesson['lesson_title'],
                "info": lesson['raw_info']
            })

    return {"research_status": "complete"}