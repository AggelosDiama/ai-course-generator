# 🎓 AI-Powered Adaptive Course Generator

An intelligent educational platform that deconstructs complex topics into structured, multi-modal learning paths. Powered by **LangGraph** for agentic workflows and **Neo4j** for graph-based knowledge management.

---

## 🚀 Features

- **Agentic Workflow**: Uses a tri-agent system (Deconstructor, Librarian, Professor) to research and create content.
- **Graph-Based Storage**: Lessons and modules are stored as nodes in Neo4j, allowing for complex relationship mapping.
- **Multi-Modal Content**: Generates theoretical explanations, professional video scripts, and module-level quizzes.
- **Interactive Roadmap**: A smooth-scrolling sidebar navigation with real-time progress tracking and scoring.
- **Tailored Expertise**: Content adjusts dynamically based on Beginner, Intermediate, or Advanced levels.

---

## 🛠️ Tech Stack

* **Frontend**: [Streamlit](https://streamlit.io/)
* **Orchestration**: [LangGraph](https://www.langchain.com/langgraph) & [LangChain](https://www.langchain.com/)
* **Database**: [Neo4j](https://neo4j.com/) (Graph Database)
* **LLM**: Groq / OpenAI (via LangChain)
* **Tools**: DuckDuckGo Search, Wikipedia API, ArXiv

---

## 🏗️ Agent Architecture

Our system utilizes three specialized agents working in a stateful graph:

1.  **The Deconstructor**: Analyzes the topic and duration to build a skeletal course structure (Syllabus).
2.  **The Librarian**: Conducts deep-dive research using web tools to gather factual "Research Dossiers" for every lesson.
3.  **The Professor**: Synthesizes research into pedagogical Markdown content, video scripts, and assessments.


---

## 🚦 Getting Started

### 1. Prerequisites
* Python 3.11+
* A running Neo4j instance
* API Keys for your LLM provider

### 2. Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd ai-course-generator

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

### 3. Environment Setup

Create a `.env` file in the root:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
GROQ_API_KEY=your_key

```

### 4. Run the App

```bash
streamlit run main.py

```

---

## 📈 Future Roadmap

* [ ] **PDF Export**: Generate a complete textbook from the course.
* [ ] **Voice Synthesis**: Turn the "Video Scripts" into actual audio files.
* [ ] **Flashcard Deck**: Auto-generate Anki-style flashcards for spaced repetition.

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

```

### 💡 Final Tip:
If you have a screenshot of your app, save it as `screenshot.png` in your folder and add `![App Screenshot](screenshot.png)` at the top of the README. Judges **love** seeing the UI before they even read the code!

**Would you like me to generate the `requirements.txt` file for you based on the libraries we've used so far?**

```