from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict, Any
import pandas as pd
from io import BytesIO, StringIO
from pydantic import BaseModel
import random


router = APIRouter()

class ColumnInfo(BaseModel):
    name: str
    dtype: str
    sample_values: List[Any]

class UploadResponse(BaseModel):
    filename: str
    columns: List[ColumnInfo]
    rows_sample: List[Dict[str, Any]]
    row_count: int
    
def try_parse_date(series: pd.Series) -> bool:
    try:
        parsed = pd.to_datetime(series.dropna().head(50), errors='coerce')
        success_ratio = parsed.notna().mean()
        return success_ratio > 0.7
    except Exception:
        return False

def detect_dtype(series: pd.Series) -> str:
    if pd.api.types.is_datetime64_any_dtype(series):
        return "date"
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    if pd.api.types.is_bool_dtype(series):
        return "boolean"
    if pd.api.types.is_object_dtype(series):
        nunique = series.nunique(dropna=True)
        total = len(series.dropna())
        if total == 0:
            return "text"
        unique_ratio = nunique / total
        
        if nunique <= 20 and unique_ratio < 0.2:
            return "categorical"
        
        #dimension
        if nunique <= 100 and unique_ratio < 0.8:
            return "dimension"
        return "text"
    return "text"

def detect_schema(df: pd.DataFrame) -> dict:
    schema = {
        "numeric": [],
        "date": [],
        "categorical": [],
        "dimension": [],
        "boolean": [],
        "text": [],
    }

    for column in df.columns:
        dtype = detect_dtype(df[column])
        schema[dtype].append(column)

    return schema


def smart_sample(df, n):
    
    if len(df) <= n:
        return df.copy()
    
    half_n = max(1, n // 2)
    
    even_idxs = [
        int(i * (len(df) - n) / (half_n - 1))
        for i in range(half_n)
    ] if half_n > 1 else [0]
    even_part = df.iloc[even_idxs]
    remaining = df.drop(even_part.index)
    
    random_part = remaining.sample(
        n=n - len(even_part), 
        replace=False
            )
    sampled_df = pd.concat([even_part, random_part])
    
    return sampled_df.sample(frac=1)

def choose_chart(schema, dataframe, main_metric):
    date_cols = schema.get("date", [])
    cat_cols = schema.get("categorical", [])

    # 1. Time chart
    if date_cols:
        return {
            "type": "line",
            "x": date_cols[0],
            "y": main_metric,
        }

    # 2. Category chart
    for col in cat_cols:
        unique_count = dataframe[col].nunique()
        if unique_count <= 20:
            return {
                "type": "bar",
                "x": col,
                "y": main_metric,
            }

    return None


@router.post("/upload/", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    content = await file.read()
    if filename.lower().endswith((".xls", ".xlsx")):
        try:
            df = pd.read_excel(BytesIO(content))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading Excel: {str(e)}")
    elif filename.lower().endswith(".csv"):
        try:
            # attempt to decode as utf-8 / fallback
            try:
                text = content.decode("utf-8")
            except UnicodeDecodeError:
                text = content.decode("latin-1")
            df = pd.read_csv(StringIO(text))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading CSV: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Use CSV or XLSX.")

    # Basic cleaning
    df = df.rename(columns=lambda c: str(c).strip())
    row_count = len(df)

    # Build columns info
    columns_info = []
    for col in df.columns:
        series = df[col]
        dtype = detect_dtype(series)
        sample = series.dropna().head(20).tolist()
        columns_info.append({
            "name": str(col),
            "dtype": dtype,
            "sample_values": sample
        })

    # Rows sample (first 50 rows but convert to native types)
    sampled_df = smart_sample(df, n=20)
    rows_sample = (
        sampled_df
        .where(pd.notnull(sampled_df), None)
        .to_dict(orient="records"
    )
    )

    return {
        "filename": filename,
        "columns": columns_info,    
        "rows_sample": rows_sample,
        "row_count": row_count
    }
