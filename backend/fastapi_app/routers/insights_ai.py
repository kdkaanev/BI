import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

client = OpenAI()

def generate_ai_insights(columns, rows):
    insights = []
    if not columns :
        return []
    
    summary = ", ".join([col["name"] for col in columns])
    
    prompt = f"""
You are a data analyst.

Based on the dataset, return ONLY valid JSON.

Format:
[
  {{
    "title": "...",
    "text": "...",
    "severity": "info"
  }}
]

Dataset summary:
Columns: {columns}
Sample rows: {rows[:5]}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
              
                {"role": "user", "content": prompt}
            ],

            temperature=0.3,
        )
        
        insights = json.loads(response.choices[0].message.content)
    except Exception as e:
         insights = [{
            "title": "AI Insight Failure",
            "text": str(e),
            "severity": "warning"
        }]
    return insights
    