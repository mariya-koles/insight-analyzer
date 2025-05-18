# 📊 Insight Analyzer

**Insight Analyzer** is a full-stack Python app that allows users to upload a CSV file, perform automatic exploratory data analysis (EDA), and receive natural-language insights powered by a free open-source LLM (Mistral via OpenRouter). It features a Streamlit frontend and a FastAPI backend.

---

## 🚀 Features

- Upload any `.csv` file from your computer
- Automatic EDA summary:
  - Data shape, column types, missing values
  - Descriptive statistics
- AI-generated insights from Mistral (via OpenRouter)
- One-click "Regenerate Insight" button
- Fully responsive and easy-to-use UI (Streamlit)

---

## 🧱 Tech Stack

| Layer      | Tech                          |
|------------|-------------------------------|
| Frontend   | [Streamlit](https://streamlit.io/) |
| Backend    | [FastAPI](https://fastapi.tiangolo.com/) |
| EDA Engine | [Pandas](https://pandas.pydata.org/), [Seaborn](https://seaborn.pydata.org/) |
| AI Model   | [Mistral-7B via OpenRouter](https://openrouter.ai) |
| Deployment | Localhost (dev environment)   |

---

## 🖥️ Project Structure

```
insight-analyzer/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── eda.py               # Pandas-based EDA logic
│   ├── llm_helper.py        # LLM (OpenRouter) integration
│   ├── uploads/             # Temp storage for CSVs
│
├── frontend/
│   └── app.py               # Streamlit user interface
│
├── .env                     # Your API keys (not tracked)
├── .gitignore               # Ignores .env, __pycache__, etc.
├── requirements.txt         # Python dependencies
└── README.md
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/insight-analyzer.git
cd insight-analyzer
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root folder:

```env
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxx
```

> ⚠️ Get your free API key from [https://openrouter.ai/keys](https://openrouter.ai/keys)

---

## ▶️ Running the App

### Run Backend (FastAPI):
```bash
uvicorn backend.main:app --reload --port 8000
```

### Run Frontend (Streamlit):
In a separate terminal:
```bash
streamlit run frontend/app.py
```

Then open: [http://localhost:8501](http://localhost:8501)

---

## 📦 Dependencies

Install them with:
```bash
pip install -r requirements.txt
```

Includes:
- `fastapi`
- `uvicorn`
- `streamlit`
- `pandas`
- `requests`
- `python-dotenv`
- `openai` (used for API-style calls via OpenRouter)

---

## 🔐 Security Notes

- Make sure your `.env` file is in `.gitignore`
- Do not expose your OpenRouter key in public repos

---

## 📌 Roadmap Ideas

- [ ] Add interactive charts (heatmaps, boxplots)
- [ ] Column selector UI
- [ ] Export insights to PDF/Markdown
- [ ] Deploy backend to Render / frontend to Streamlit Cloud


