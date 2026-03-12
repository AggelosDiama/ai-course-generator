import json
from src.utils.helpers import load_prompt
from src.logger.logger import get_logger

logger = get_logger("Discovery")

def discovery_agent(state, llm, db):
    logger.info(f"Checking for existing courses similar to: {state['topic']}")
    
    # 1. Fetch existing courses
    existing_courses = db.get_all_course_metadata()
    if not existing_courses:
        return {"exists": False}

    # 2. Ask the LLM to perform semantic matching
    template = """
    You are a Semantic Router. Compare the user's request with the existing courses list.
    
    USER REQUEST:
    - Topic: {topic}
    - Expertise: {expertise}
    - Duration: {duration} hours
    - Interests: {interests}
    
    EXISTING COURSES:
    {existing_list}
    
    CRITERIA:
    - Topic is semantically the same (e.g., "Math" vs "Mathematics").
    - Expertise level matches exactly.
    - Duration is within +/- 20% of the requested time.
    - Interests are closely related.

    If a match exists, return the EXACT 'title' of the existing course.
    If no match, return "NONE".
    
    Return ONLY JSON: {{"match_found": true/false, "existing_title": "Title or NONE"}}
    """
    
    res = llm.invoke(template.format(
        topic=state['topic'],
        expertise=state['expertise'],
        duration=state['duration'],
        interests=state['interests'],
        existing_list=str(existing_courses)
    ))
    
    try:
        data = json.loads(res.content.replace("```json", "").replace("```", "").strip())
        if data["match_found"]:
            logger.info(f"🎯 Semantic match found: {data['existing_title']}")
            return {"exists": True, "topic": data["existing_title"]}
    except:
        pass

    return {"exists": False}