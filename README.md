# 🎓 AI-Powered Adaptive Course Generator

An intelligent, self-hosted educational platform that deconstructs complex topics into structured, multi-modal learning paths. Powered by **LangGraph** for agentic workflows and **Neo4j** for graph-based knowledge management.

---

## 🚀 Key Updates & Features

* **Local-First AI**: Runs entirely on your machine using **Ollama (Llama 3.2)**—no API keys required for core generation.
* **Unified Proxy**: Uses **LiteLLM** to provide an OpenAI-compatible interface for local models, ensuring high reliability and easy model swapping.
* **Semantic Discovery**: A new **Discovery Agent** checks the Neo4j database before generation. If a semantically similar course exists for your expertise level, it loads instantly instead of re-generating.
* **Agentic Workflow**: A four-agent system (Discovery, Deconstructor, Librarian, Professor) to research and create content.
* **Graph-Based Storage**: Lessons and modules are stored as nodes in Neo4j, allowing for complex relationship mapping and progress persistence.
* **Interactive Roadmap**: Smooth-scrolling sidebar navigation with real-time progress tracking and scoring.
* **Progress Reset**: Ability to wipe quiz scores and "completed" status to retake courses from scratch.

---

## 🛠️ Tech Stack

* **Frontend**: [Streamlit](https://streamlit.io/)
* **Orchestration**: [LangGraph](https://www.langchain.com/langgraph) & [LangChain](https://www.langchain.com/)
* **Local LLM**: [Ollama](https://ollama.com/) (Llama 3.2)
* **API Proxy**: [LiteLLM](https://github.com/BerriAI/litellm)
* **Database**: [Neo4j](https://neo4j.com/) (Graph Database)
* **Package Manager**: [uv](https://github.com/astral-sh/uv) (Inside Docker for 10x faster builds)
* **Tools**: DuckDuckGo Search, Wikipedia API, ArXiv

---

## 🏗️ Agent Architecture

1. **The Discovery Agent**: Semantically matches user intent against existing Neo4j records to prevent duplicate generation.
2. **The Deconstructor**: Analyzes the topic and duration to build a skeletal course structure (Syllabus).
3. **The Librarian**: Conducts deep-dive research using web tools to gather factual "Research Dossiers" for every lesson.
4. **The Professor**: Synthesizes research into pedagogical Markdown content, video scripts, and assessments.

---

## 🚦 Getting Started (Dockerized)

The entire stack is orchestrated via Docker Compose, including the LLM, Database, and Proxy.

### 1. Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.
* **Important**: Assign at least **8GB of RAM** to Docker in *Settings > Resources*.

### 2. Installation & Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd ai-course-generator

# Ensure your .env matches the Docker network (see below)

```

### 3. Environment Setup (`.env`)

Create a `.env` file in the root:

```env
AI_API_KEY=my-secret-key
AI_ENDPOINT=http://litellm:4000/v1
AI_MODEL=gpt-4-turbo

NEO4J_URI=bolt://neo4j-db:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=P@ssword1234

```

### 4. Run with One Command

```bash
docker compose -f docker/docker-compose.yml up --build

```

*Note: The first run will take a few minutes as it pulls the Llama 3.2 model (~2GB) and the all-minilm embedding model.*

---

## 📂 Project Structure

```text
.
├── docker/                 # Docker Compose & LiteLLM configs
├── src/
│   ├── agents/             # Discovery, Librarian, etc.
│   ├── database/           # Neo4j operations
│   ├── graph/              # LangGraph definition
│   ├── logger/             # Local logging & log files
│   ├── ui/                 # Streamlit components
│   └── main.py             # Entry point
├── Dockerfile              # uv-optimized build
└── requirements.txt        # Python dependencies

```

---

## 📈 Future Roadmap

* [x] **Local LLM Support**: Completed via Ollama.
* [x] **Semantic Search**: Completed via Discovery Agent.
* [ ] **PDF Export**: Generate a complete textbook from the course.
* [ ] **Voice Synthesis**: Turn the "Video Scripts" into actual audio files using Bark or Coqui.

