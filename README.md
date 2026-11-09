# AI Learning Journey: Simple AI Assistant with RAG

A hands-on project built while learning AI/LLM development through a video playlist. It grows step by step from simple experiments (streaming, embeddings) to a small AI assistant that can call tools and answer questions from a local knowledge base using semantic search.

> **Status:** Work in progress. More features and cleanup coming as I keep learning.

## Features

- **Simple AI assistant** (`simple_ai_assistant.py`) – main entry point for the chat assistant
- **Tool calling** (`tools.py`) – functions the assistant can call
- **Semantic search / RAG** – documents are embedded and stored in a local vector store (`vector_store.json`), then searched to ground the assistant's answers
- **Streaming responses** – experiments with streaming output and streaming with tools
- **Knowledge base** – sample HR / policy / tech documents used for retrieval

## Project Structure

```
first/
├── code_snippets/            # Small experiments from each lesson
│   ├── chunk_search.py       # Chunking + searching text
│   ├── doc_search.py         # Searching across documents
│   ├── semantic_search_test.py
│   ├── stream_test.py        # Streaming responses
│   ├── stream_tools_test.py  # Streaming + tool calls
│   └── test_embedding.py     # Generating embeddings
├── knowledge_base/           # Documents the assistant can search
│   ├── hiring_process.txt
│   ├── hr_docs.txt
│   ├── leave_policy.txt
│   ├── medical_policy.txt
│   ├── rca_docs.txt
│   ├── tech_docs.txt
│   ├── travel_expense.txt
│   └── vector_store.json     # Stored embeddings
├── Utilities/
│   └── utilities.py          # Shared helper functions
├── simple_ai_assistant.py    # Main assistant script
├── tools.py                  # Tool definitions
├── .env                      # API keys (NOT committed)
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9+
- An API key for your LLM / embedding provider

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file in the project root:

```env
API_KEY=your_api_key_here
```

> Replace `API_KEY` with the variable name your code actually reads. Never commit this file.

### Run

```bash
python simple_ai_assistant.py
```

To try individual lessons:

```bash
python code_snippets/semantic_search_test.py
python code_snippets/stream_test.py
```

## How It Works

1. Documents in `knowledge_base/` are split into chunks.
2. Each chunk is converted into an embedding and saved in `vector_store.json`.
3. When you ask a question, it is embedded and compared against the stored vectors.
4. The most relevant chunks are passed to the LLM as context to generate the answer.
5. If needed, the assistant calls functions defined in `tools.py`.

## Roadmap

- [ ] Clean up and document each code snippet
- [ ] Add `requirements.txt` and usage examples
- [ ] Add more tools
- [ ] Add a simple UI (CLI / web)
- [ ] Add tests

## Acknowledgements

Built while following an AI learning playlist.

