# Document Portal

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/rohitsmagdum13/Document_Portal.git
cd Document_Portal
```

### 2. Set Up Conda Virtual Environment

```bash
# Create virtual environment with Python 3.10
conda create -p venv python=3.10 -y

# Activate the environment
conda activate venv/
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in your project root:

```bash
# LLM API Keys (choose one or more)
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
CLAUDE_API_KEY=your_claude_api_key
HUGGINGFACE_API_KEY=your_hf_api_key

# Vector Database Configuration
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=your_pinecone_env
WEAVIATE_URL=your_weaviate_url
QDRANT_URL=your_qdrant_url
```

## Minimum Requirements

### 1. LLM Models
Choose one of the following:

- **Groq** (Free) - Fast inference API
- **OpenAI** (Paid) - GPT-3.5/GPT-4 models
- **Gemini** (15 days free access) - Google's LLM
- **Claude** (Paid) - Anthropic's AI assistant
- **Hugging Face** (Free) - Open source models
- **Ollama** (Local setup) - Run models locally

### 2. Embedding Models
Select an embedding model:

- **OpenAI Embeddings** - text-embedding-ada-002
- **Hugging Face Embeddings** - sentence-transformers models
- **Gemini Embeddings** - Google's embedding API

### 3. Vector Database Options

#### In-Memory
- **FAISS** - Fast similarity search
- **Chroma** - Simple in-memory vector store
- **Numpy/Pandas** - Basic array operations

#### On-Disk
- **FAISS with persistence** - Save/load indices
- **Chroma with persistence** - Local file storage
- **SQLite with vector extensions**

#### Cloud-Based
- **Pinecone** - Managed vector database
- **Weaviate** - Open source, cloud deployment
- **Qdrant** - High-performance vector search
- **MongoDB Atlas Vector Search**
- **PostgreSQL with pgvector**

## Notes

- Add your `.env` file to `.gitignore` to keep API keys secure
- Always ensure your virtual environment is activated before installing packages or running the project

## Deactivating Environment

```bash
conda deactivate
```