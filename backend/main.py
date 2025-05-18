from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
from backend.eda import run_basic_eda
from backend.llm_helper import get_llm_insight

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    file_location = UPLOAD_DIR / file.filename
    with file_location.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "message": "File uploaded successfully."}


@app.get("/analyze")
def analyze_csv(filename: str = Query(..., description="Name of uploaded CSV file")):
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="CSV file not found.")

    try:
        # Step 1: Run EDA
        eda_result = run_basic_eda(str(file_path))

        # Step 2: Create prompt for LLM
        prompt = f"""
You are a data science assistant. Analyze this dataset summary:

Shape: {eda_result['shape']}
Columns: {eda_result['columns']}
Dtypes: {eda_result['dtypes']}
Missing values: {eda_result['missing']}

Statistical summary:
{eda_result['describe']}

Provide insights about trends, issues, or recommendations.
"""
        # Step 3: Get insight
        insight = get_llm_insight(prompt)

        return {
            "eda": eda_result,
            "insight": insight
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
