# AIOps Log Analyzer

A minimal AI-powered log analysis demo for CloudOps.

This project demonstrates how a simple AI service can analyze application failure logs and return a structured incident summary.

## Architecture

```text
Dummy App
   ↓
Failure Logs
   ↓
AI Analyzer API
   ↓
Structured Incident Summary
```

## Components
- ```dummy-app```: Flask app with intentional failure endpoints
- ```ai-analyzer```: FastAPI service that sends logs to an LLM
- ```examples```: sample logs for testing

## Run Locally
- Create ```.env```:
```
cp .env.example .env
```

Add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

Start services:
```
docker compose up --build
```

## Trigger Dummy Failure
```
curl http://localhost:5000/fail/divide
```

Check logs:
```
docker logs aiops-dummy-app
```

## Analyze Logs
```
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "logs": "ZeroDivisionError: division by zero at /fail/divide endpoint"
  }'
```

## Example Response
```
{
  "summary": "The dummy application failed because it attempted to divide by zero.",
  "severity": "medium",
  "probable_cause": "Unhandled arithmetic exception in the /fail/divide endpoint.",
  "affected_component": "dummy-app",
  "recommended_actions": [
    "Add input validation before division",
    "Handle ZeroDivisionError exceptions",
    "Add automated tests for failure scenarios"
  ]
}
```

## Skills Demonstrated
- AI API integration
- Prompt engineering
- Structured JSON output
- FastAPI service development
- Docker Compose workflow
- CloudOps-style incident analysis

## Future Improvements
- Add Azure Container Apps deployment
- Add Azure Log Analytics integration
- Add Key Vault for secret management
- Add runbook-based RAG
- Add response evaluation tests
