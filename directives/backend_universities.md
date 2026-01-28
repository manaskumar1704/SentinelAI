# Backend Universities Directive

## Purpose

Search, recommend, and manage university shortlists.

## Inputs

- Search: name, country filters
- Recommendations: user profile from onboarding
- Shortlist: university selection + category

## Process

### Search

1. Query Hipo University API
2. Transform response to `University` model
3. Return matching universities

### Recommendations

1. Get preferred countries from profile
2. Fetch universities per country
3. Categorize as Dream/Target/Safe
4. Calculate acceptance chances
5. Generate fit reasons and risks

### Shortlist/Lock

1. Validate university exists
2. Add to user's shortlist
3. Lock to unlock application guidance

## Tools/Scripts

- `routers/universities.py` - API endpoints
- `services/universities.py` - Business logic
- `models/university.py` - Data models

## External API

- URL: `http://universities.hipolabs.com`
- Endpoints:
  - `/search?name=xxx` - Search by name
  - `/search?country=xxx` - Filter by country

## Outputs

- List of universities
- Categorized recommendations
- Shortlist with lock status

## Edge Cases

- API timeout → Empty list
- University not found → 404
- Already shortlisted → 400
- Remove locked → 400 (must unlock first)
