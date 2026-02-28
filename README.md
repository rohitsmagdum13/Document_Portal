# Document Portal

A document processing and Q&A portal built with LangChain, FastAPI, and Streamlit.

## Steps Completed

### Step 1: Project Initialization

- Created a new project using **uv** package manager (`uv init`).
- This generated:
  - `pyproject.toml` — project metadata and dependency declarations
  - `main.py` — entry point with a basic `Hello from document-portal!` script
  - `.python-version` — pinned Python version to **3.12**
  - `.gitignore` — ignoring `__pycache__/`, `.venv/`, `.env`, build artifacts, etc.

### Step 2: Virtual Environment Setup

- Created a Python virtual environment (`.venv/`) using uv.
- All dependencies are resolved and locked in `uv.lock`.

### Step 3: Dependency Installation

- Installed all required packages via `requirements.txt` and `pyproject.toml`:

  | Package                | Version        | Purpose                        |
  |------------------------|----------------|--------------------------------|
  | langchain              | 0.3.27         | LLM orchestration framework    |
  | langchain-community    | 0.3.27         | Community integrations         |
  | langchain-core         | 0.3.72         | Core LangChain abstractions    |
  | langchain-groq         | 0.3.6          | Groq LLM integration           |
  | langchain-google-genai | 2.1.8          | Google Generative AI integration|
  | faiss-cpu              | 1.11.0.post1   | Vector similarity search       |
  | fastapi                | 0.116.1        | Backend API framework          |
  | uvicorn                | 0.35.0         | ASGI server for FastAPI        |
  | python-dotenv          | 1.1.1          | Environment variable management|
  | python-multipart       | 0.0.20         | File upload support            |
  | PyMuPDF                | 1.26.3         | PDF parsing                    |
  | pypdf                  | 5.8.0          | PDF reading                    |
  | docx2txt               | 0.9            | DOCX file text extraction      |
  | loguru                | 0.7.3          | Logging utility                |
  | streamlit              | 1.47.1         | Frontend UI                    |
  | ipykernel              | 6.30.0         | Jupyter notebook support       |
  | pytest                 | 8.4.1          | Testing framework              |
  | cfn-lint               | >=1.45.0       | CloudFormation linting         |

### Step 4: Environment Configuration

- Created a `.env` file for storing API keys and secrets (excluded from version control via `.gitignore`).

### Step 5: Git Configuration & Version Control

- Initialized a Git repository.
- Configured Git user name and email.
- Made the first commit: **"Project Folder Initialize"**.
- Added remote origin: `https://github.com/rohitsmagdum13/Document_Portal.git`
- Pushed the initial commit to the `master` branch.

### Step 6: Project Folder Structure Creation

- Created `setup_project.py` — a script that generates the entire project structure.
- Ran the script to create all folders and files:

```
Document_Portal/
├── logging/                  # Custom logging module
│   ├── __init__.py
│   └── custom_logger.py
├── exception/                # Custom exception handling
│   ├── __init__.py
│   └── custom_exception.py
├── src/                      # Core source modules
│   ├── __init__.py
│   ├── doc_compare/          # Document comparison
│   ├── doc_analyzer/         # Document analysis
│   ├── multi_doc_chat/       # Multi-document chat
│   └── single_doc_chat/      # Single-document chat
├── utils/                    # Utility helpers
│   ├── __init__.py
│   └── llm_utils.py
├── notebook/                 # Jupyter notebooks
│   └── experiments.ipynb
├── config/                   # Configuration files
│   └── config.yaml
├── prompt/                   # Prompt templates
│   ├── __init__.py
│   └── prompt_library.py
├── template/                 # HTML templates
│   └── index.html
├── static/                   # Static assets
│   └── style.css
├── app.py                    # FastAPI backend
└── streamlit_ui.py           # Streamlit frontend
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/rohitsmagdum13/Document_Portal.git
cd Document_Portal

# Create virtual environment and install dependencies
uv sync

# Create a .env file and add your API keys
cp .env.example .env
```

### Running the Application

```bash
# Run the main script
uv run python main.py
```
