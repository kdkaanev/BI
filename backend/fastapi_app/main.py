from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import data, insights
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = FastAPI(title="BI FastAPI Microservice")

# Allow local dev origins (adjust in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your domains for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router, prefix="/data", tags=["data"])
app.include_router(insights.router, prefix="/insights", tags=["insights"])


print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY")[:10])
print("FastAPI BI microservice is running...")