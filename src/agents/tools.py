import wikipedia
import requests
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

def search_wikipedia(lesson: str) -> str:
    try: 
        return wikipedia.summary(lesson, sentences=3)
    except: 
        return f"Wikipedia content for {lesson} not available."

def search_duckduckgo(lesson: str) -> str:
    try: 
        wrapper = DuckDuckGoSearchAPIWrapper(max_results=2)
        return wrapper.run(lesson)
    except: 
        return "Web search info unavailable."

def search_arxiv(lesson: str) -> str:
    """Searches ArXiv for academic papers related to the lesson."""
    try:
        url = f"http://export.arxiv.org/api/query?search_query=all:{lesson}&max_results=2"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            # Returning raw text snippet; the Professor LLM is good at parsing this
            return response.text[:1000] 
        return "No academic papers found on ArXiv."
    except Exception as e:
        return f"ArXiv search failed: {str(e)}"