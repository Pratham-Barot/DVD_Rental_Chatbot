# DVD Rental Chatbot

Natural-language assistant for the classic **PostgreSQL DVD Rental** database. Ask questions in plain English; the app routes them through a LangGraph workflow, retrieves schema context with RAG, generates and validates SQL, runs safe read-only queries, and returns clear answers in a Streamlit chat UI.

## Features

- **Streamlit chat UI** — conversational interface with sidebar and clear-chat
- **LangGraph workflow** — routes general chat, schema questions, and SQL questions
- **RAG over schema** — ChromaDB + Gemini embeddings for relevant table/column context
- **SQL generation & repair** — Gemini generates SQL; failed queries can be auto-fixed
- **Guardrails** — input checks, intent filtering, SQL validation (allowed tables, limits, no destructive ops), sensitive-column protection, and output validation
- **PostgreSQL** — connects to the DVD Rental sample schema (`actor`, `film`, `rental`, `payment`, etc.)

## Architecture

```
User question
    → Input guardrail
    → LangGraph router
        ├─ chat              (general / ML questions)
        ├─ schema_chat       (schema explanation)
        └─ SQL path
              retrieve schema (RAG)
              → generate SQL
              → validate SQL
              → execute SQL
              → fix SQL (on error)
              → generate answer
    → Output guardrail
    → Streamlit response
```

| Area | Path |
|------|------|
| App entry | `app.py` |
| Workflow | `graph/` |
| LLM / SQL | `ai/` |
| RAG | `rag/` |
| DB access | `database/` |
| Safety | `guardrails/`, `security/` |
| UI | `pages/`, `components/` |

## Prerequisites

- Python 3.10+
- PostgreSQL with the [DVD Rental](https://www.postgresqltutorial.com/postgresql-getting-started/postgresql-sample-database/) sample database loaded
- A [Google Gemini](https://ai.google.dev/) API key

## Setup

```bash
git clone https://github.com/Pratham-Barot/DVD_Rental_Chatbot.git
cd DVD_Rental_Chatbot

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file in the project root (never commit this file):

```env
GEMINI_API_KEY=your_gemini_api_key

DB_HOST=localhost
DB_PORT=5432
DB_NAME=dvdrental
DB_USER=your_db_user
DB_PASSWORD=your_db_password

# Optional LangSmith tracing
LANGCHAIN_TRACING_V2=false
LANGCHAIN_PROJECT=dvd-rental-chatbot
```

## Run

```bash
streamlit run app.py
```

Open the URL Streamlit prints (usually `http://localhost:8501`) and ask questions such as:

- How many films are in the database?
- Which actors appear in the most films?
- What tables are related to rentals?
- Explain what the payment table stores.

## Project structure

```
├── app.py                 # Streamlit entrypoint
├── main.py                # Simple CLI-style ask_assistant helper
├── ai/                    # LLM client, prompts, SQL generate/fix
├── agents/                # SQL agent helpers
├── graph/                 # LangGraph state, nodes, workflow
├── rag/                   # Schema docs, Chroma vector store, retriever
├── database/              # Postgres connection, schema reader, executor
├── guardrails/            # Input, intent, SQL, sensitive, output checks
├── security/              # Secure SQL tooling
├── pages/                 # Chat page
├── components/            # Sidebar
├── chroma_db/             # Local vector store data
├── requirements.txt
└── .env                   # Local secrets (gitignored)
```

## Safety notes

- Queries are constrained to an allowlist of DVD Rental tables.
- Destructive SQL and unbounded result sets are blocked or limited.
- Sensitive columns are filtered by guardrails.
- Keep `.env` and DB credentials out of git (already covered by `.gitignore`).

## Tests

```bash
python test_sql_validator.py
python test_sensitive_guardrail.py
python test_select_star.py
python test_error_handler.py
python test_memory_fix.py
python test_memory_growth.py
```

## Tech stack

- **UI:** Streamlit  
- **Orchestration:** LangGraph / LangChain  
- **LLM:** Google Gemini  
- **Vector store:** ChromaDB  
- **Database:** PostgreSQL (DVD Rental)  
- **Config:** python-dotenv  

## License

This project is for learning and demonstration purposes.
