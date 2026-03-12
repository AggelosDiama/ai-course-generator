import json
from langchain_core.prompts import ChatPromptTemplate
from database.neo4j_ops import Neo4jManager
from utils.helpers import load_prompt
from src.logger.logger import get_logger

logger = get_logger("Deconstructor")
db = Neo4jManager()

def deconstructor_agent(state, llm):
    logger.info(f"🚀 Starting deconstruction for topic: {state['topic']}")

    template_str = load_prompt("deconstructor.txt")
    prompt = ChatPromptTemplate.from_template(template_str)
    
    chain = prompt | llm
    response = chain.invoke({
        "topic": state['topic'],
        "expertise": state['expertise'],
        "duration": state['duration'],
        "interests": state['interests']
    })
    
    content = response.content.replace("```json", "").replace("```", "").strip()
    data = json.loads(content)
    
    # We pass the original state['topic'] so Neo4j knows which node to MERGE/CREATE
    db.save_course_structure(data, state['topic'], state['expertise'], state['duration'], state['interests'])

    logger.info(f"✅ Structure created for '{data['course_title']}'. Saved to Neo4j.")
    return {"course_data": data}

