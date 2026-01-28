# Backend Onboarding Directive

## Purpose

Manage user onboarding data collection and validation.

## Inputs

- User ID from auth middleware
- Onboarding form data (academic, goals, budget, exams)

## Process

1. Validate all required sections via Pydantic models
2. Store onboarding data (in-memory for MVP)
3. Calculate completion percentage
4. Unlock AI Counsellor when complete

## Tools/Scripts

- `routers/onboarding.py` - API endpoints
- `services/onboarding.py` - Business logic
- `models/onboarding.py` - Data models

## Outputs

- `OnboardingStatus` with completion info
- Profile data for AI context

## Edge Cases

- Partial updates require existing data
- All sections mandatory for completion
- Empty sections → 0% completion

## Data Sections (per PLAN.md)

1. Academic Background
2. Study Goals
3. Budget
4. Exams & Readiness
