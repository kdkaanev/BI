from http import client
import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict, List
from collections import Counter
from .generate_insights import generate_insights, generate_kpis
from .insights_ai import generate_ai_insights
from .charts import build_main_chart
from .data import detect_dtype, detect_schema
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
import os
print("OPENAI KEY EXISTS?", bool(os.getenv("OPENAI_API_KEY")))



router = APIRouter()


# Модели за request/response
class InsightsRequest(BaseModel):
   columns: List[Dict[str, Any]]
   rows_sample: List[Dict[str, Any]]
   

class Insight(BaseModel):
    title: str
    text: str
    severity: str = "info"
    source: str #"classic" or "ai" 
    
class InsightsResponse(BaseModel):
    insights: List[Insight]

@router.post("/analyze")
async def analyze_insights(payload: InsightsRequest):
    df = pd.DataFrame(payload.rows_sample)
    
    schema = detect_schema(df)

    columns = payload.columns
    rows_sample = payload.rows_sample
    
    
    classic_insights = generate_insights(columns, rows_sample)
    classic_kpis = generate_kpis(columns, rows_sample)
    main_chart = build_main_chart(df, schema)
    
    try:
        ai_insights = generate_ai_insights(columns, rows_sample)
        if ai_insights is None:
            ai_insights = []
    except Exception as e:
        ai_insights = [{
            "title": "AI Insight Failure",
            "text": str(e),
            "severity": "warning"
        }]
    return {
        "insights": classic_insights,
        "kpis": classic_kpis,
        "chart": main_chart,
    }

    
    