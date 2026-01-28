# Backend AI Counsellor Directive

## Purpose

Provide AI-powered study abroad counselling via Groq API.

## Inputs

- User messages (chat history)
- User profile from onboarding (auto-injected)

## Process

1. Verify onboarding complete (gate access)
2. Build system prompt with user context
3. Call Groq API with llama-3.3-70b-versatile
4. Return AI response (streaming optional)

## Tools/Scripts

- `routers/counsellor.py` - API endpoints
- `services/groq_client.py` - Groq integration

## Outputs

- AI response text
- Streaming SSE for real-time responses

## Edge Cases

- Onboarding incomplete → 403 Forbidden
- Groq rate limit → Retry with backoff
- Empty context → Generic counselling mode

## Model Configuration

- Model: `llama-3.3-70b-versatile`
- Temperature: 0.7
- Max tokens: 1024

## System Prompt Includes

- Counsellor persona
- User's academic background
- Study goals and preferences
- Budget constraints
- Exam readiness status
