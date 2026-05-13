import json
import os

from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import ValidationError

from prompts import SYSTEM_PROMPT
from schemas import AnalyzeRequest, AnalyzeResponse

app = FastAPI(title="AIOps Log Analyzer")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.get("/")
def health_check():
    return {"status": "ok", "service": "ai-analyzer"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_logs(request: AnalyzeRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured")

    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0.2,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Analyze these logs:\n\n{request.logs}"
                }
            ],
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        parsed = json.loads(content)

        return AnalyzeResponse(**parsed)

    except json.JSONDecodeError:
        raise HTTPException(status_code=502, detail="AI returned invalid JSON")

    except ValidationError as error:
        raise HTTPException(status_code=502, detail=f"AI response failed validation: {error}")

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
