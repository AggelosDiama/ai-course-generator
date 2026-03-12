from typing import TypedDict, Dict, Any

class CourseState(TypedDict):
    topic: str
    expertise: str
    duration: int
    interests: str
    course_data: Dict[str, Any]
    final_content: str