# ai-analytics-assistant

# AI Analytics Assistant

Ask questions about your sales data in plain English and get back 
charts instantly. The system converts your question to SQL, runs it 
against a real database, and renders the result as a bar chart, 
line chart, pie chart, or table — automatically.

**Live Demo:** [ai-analytics-assistant-xg5m.vercel.app](https://ai-analytics-assistant-xg5m.vercel.app)  
**API Docs:** [ai-analytics-assistant.onrender.com/docs](https://ai-analytics-assistant.onrender.com/docs)

---

## How It Works

```
User types: "What are total sales by region?"
        │
        ▼
FastAPI receives the question
        │
        ▼
Groq LLM converts it to SQL:
SELECT r.name, SUM(s.amount) as total_sales
FROM sales s JOIN regions r ON s.region_id = r.id
GROUP BY r.name ORDER BY total_sales DESC
        │
        ▼
SQL validated (SELECT only — no destructive operations)
        │
        ▼
SQLite executes the query
        │
        ▼
Chart builder detects: one text column + one numeric = bar chart
        │
        ▼
React renders a bar chart using Recharts
```

---

## Sample Questions to Try

- *What are total sales by region?* → Bar chart
- *Show monthly revenue trend for 2024* → Line chart
- *Which product category generates the most revenue?* → Pie chart
- *What are the top 5 products by total sales?* → Bar chart
- *Show me all sales above 500,000 naira* → Table

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Text-to-SQL | Groq — Llama 3.3 70B | Natural language → SQL |
| Database | SQLite + SQLAlchemy | 18 months of sales data |
| Chart detection | Custom Python logic | Picks right chart for the data |
| Backend | FastAPI | REST API |
| Frontend | React + Vite | Single-page app |
| Charts | Recharts | Bar, line, pie chart components |
| Styling | Tailwind CSS | Utility-first styling |
| Containerisation | Docker + Docker Compose | Environment parity |
| Backend hosting | Render | FastAPI via Docker |
| Frontend hosting | Vercel | React/Vite native deployment |

---

## Key Engineering Decisions

**Why schema-aware prompting?**
The LLM cannot write correct SQL without knowing your database structure.
The system prompt includes every table name, column name, data type, and
relationship. This is the difference between SQL that works and SQL that
hallucinates table names.

**Why validate SQL before running it?**
LLMs can be manipulated into generating destructive SQL. A hard validation
layer rejects any query that does not start with SELECT before it reaches
the database — regardless of how the LLM responded.

**Why separate the chart builder from the query runner?**
The query runner does not know about charts. The chart builder does not
know about SQL. Each component has one job. Swapping Recharts for a
different charting library means changing only the React component —
the backend chart builder stays the same.

**Why send `x_key` and `y_keys` from the backend?**
The backend knows the data structure — it generated the SQL and saw the
results. Making the frontend guess which columns are axes would be fragile.
The backend tells React exactly what to render.

---

## Project Structure

```
ai-analytics-assistant/
├── backend/
│   ├── app/
│   │   ├── api/routes/
│   │   │   ├── query.py        # /ask and /samples endpoints
│   │   │   └── health.py       # GET /health
│   │   ├── api/schemas.py      # Request/response models
│   │   ├── core/
│   │   │   ├── sql_generator.py  # LLM text-to-SQL
│   │   │   ├── query_runner.py   # SQL validation + execution
│   │   │   └── chart_builder.py  # Chart type detection + formatting
│   │   ├── db/
│   │   │   ├── models.py       # SQLAlchemy table definitions
│   │   │   └── database.py     # Engine, sessions, raw query runner
│   │   ├── services/
│   │   │   └── analytics_service.py  # Pipeline orchestration
│   │   └── main.py             # FastAPI app factory
│   └── scripts/seed_data.py    # 18 months of Nigerian sales data
├── frontend/
│   └── src/
│       ├── api/client.js       # Axios HTTP client
│       ├── components/
│       │   ├── QueryInput.jsx    # Controlled input form
│       │   ├── SampleQuestions.jsx  # Clickable sample chips
│       │   ├── ChartDisplay.jsx  # Recharts bar/line/pie/table
│       │   └── SqlDisplay.jsx    # Collapsible SQL block
│       └── App.jsx              # Root component, state management
├── Dockerfile
├── Dockerfile.frontend
├── docker-compose.yml
├── nginx.conf
└── .python-version
```

---

## Running Locally

### Prerequisites
- Python 3.12+
- Node.js 20+
- [Groq](https://console.groq.com) free API key

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add GROQ_API_KEY to .env
python scripts/seed_data.py
uvicorn app.main:app --reload --port 8000
```

### Frontend (new terminal)

```bash
cd frontend
npm install
# Create .env with: VITE_API_URL=http://localhost:8000
npm run dev
```

Visit `http://localhost:5173`

### With Docker

```bash
docker compose up --build
```

Backend at `http://localhost:8000/docs`  
Frontend at `http://localhost:80`

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/query/ask` | Ask a question, get chart data |
| `GET` | `/api/v1/query/samples` | Get sample questions |
| `GET` | `/health` | Health check |

---

## Running Tests

```bash
cd backend
python -m pytest tests/ -v
```

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GROQ_API_KEY` | ✅ | — | Groq API key |
| `LLM_MODEL` | ❌ | `llama-3.3-70b-versatile` | Groq model |
| `DATABASE_URL` | ❌ | auto-computed | SQLite path |
| `APP_ENV` | ❌ | `development` | Environment name |

Frontend (set in Vercel or `.env`):

| Variable | Description |
|---|---|
| `VITE_API_URL` | Your Render backend URL |

---

## Author

**Mubarak Olalekan Oladipo**  
AI Software Engineer  
[GitHub](https://github.com/Mubrix2) · [LinkedIn](https://linkedin.com/in/mubarak-oladipo)
