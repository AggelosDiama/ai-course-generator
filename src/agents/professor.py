import json
import os
from langchain_core.prompts import ChatPromptTemplate
from database.neo4j_ops import Neo4jManager
from utils.helpers import load_prompt
from src.logger.logger import get_logger

logger = get_logger("Professor")
db = Neo4jManager()

def professor_agent(state, llm):
    logger.info(f"🎓 Professor generating content via .txt prompt for: {state['topic']}")
    
    template_str = load_prompt("professor.txt")

    # 2. Get expertise-specific instructions
    expertise_map = {
        "Beginner": "Use simple language, plenty of analogies, and avoid assuming prior knowledge.",
        "Intermediate": "Use technical terms, provide real-world applications, and assume basic familiarity.",
        "Advanced": "Deep dive into theoretical frameworks, edge cases, and architectural considerations."
    }
    exp_instr = expertise_map.get(state['expertise'], "Provide a balanced overview.")

    # 3. Fetch context from Neo4j
    ctx = db.graph.query("""
        MATCH (c:Course)-[:HAS_MODULE]->(m:Module)-[:HAS_LESSON]->(l:Lesson)
        WHERE c.title = $t OR c.generated_title = $t
        RETURN m.title as module, l.title as lesson, l.info as research
    """, params={"t": state['topic']})

    # 4. Create the prompt template
    prompt = ChatPromptTemplate.from_template(template_str)
    chain = prompt | llm
    
    res = chain.invoke({
        "topic": state['topic'],          
        "duration": state['duration'],    
        "interests": state["interests"],
        "expertise": state["expertise"],
        "context": str(ctx),
        "expertise_instruction": exp_instr
    })

    # 6. Parse and Save
    try:
        json_data = json.loads(res.content.replace("```json", "").replace("```", "").strip())
        db.save_final_json(state['topic'], json_data)
        logger.info("✅ Professor finished. Course saved to Neo4j.")
        return {"final_content": json_data}
    except Exception as e:
        logger.error(f"❌ Failed to parse Professor JSON: {e}")
        return {"final_content": {}}