# Portfolio — API Contracts & Integration Plan

## Scope
Replace frontend mock data (from `/app/frontend/src/mock.js`) with real backend endpoints using FastAPI + MongoDB. The contact form will persist to MongoDB.

## Data currently in `mock.js`
- `profile` (name, handle, role, location, email, tagline, bio, avatar, resumeUrl, stats[], socials[])
- `experience` (array)
- `education` (array)
- `skillGroups` (array of { category, items[{name, level}] })
- `projects` (array of { id, title, category, description, tech[], image, github, demo, featured })
- `projectCategories` (derived on frontend from projects)
- `CONTACT_STORAGE_KEY` (localStorage key — removed after integration)

## Backend Endpoints (all prefixed with `/api`)

### 1. GET `/api/portfolio`
Returns the full portfolio payload in one call to minimize round-trips.
```json
{
  "profile": { ...profile fields... },
  "experience": [ ... ],
  "education": [ ... ],
  "skillGroups": [ ... ],
  "projects": [ ... ]
}
```
Status: 200 OK. On startup, DB is seeded with current mock data if empty.

### 2. POST `/api/contact`
Body:
```json
{ "name": "string (1-80)", "email": "valid email", "message": "string (10-5000)" }
```
Response 200:
```json
{ "id": "uuid", "status": "received", "ts": "ISO datetime" }
```
Validation errors → 422.

### 3. GET `/api/contact` (optional, simple)
Returns list of submissions (recent first). For demo/admin view.
```json
[ { "id", "name", "email", "message", "ts" }, ... ]
```

## MongoDB Collections
- `portfolio_profile` — single doc with profile
- `portfolio_experience` — docs
- `portfolio_education` — docs
- `portfolio_skill_groups` — docs (category + items)
- `portfolio_projects` — docs
- `contact_messages` — docs (id, name, email, message, ts)

## Seeding
On app startup, if `portfolio_profile` is empty, seed all portfolio collections with the same data currently in the frontend `mock.js` so the first request returns populated content.

## Frontend Integration Steps
1. Create `/app/frontend/src/api.js` — axios client with `BACKEND_URL + /api`.
2. Replace imports of `profile`, `experience`, `education`, `skillGroups`, `projects`, `projectCategories` from `mock.js` with a single `usePortfolio()` hook that fetches `/api/portfolio` once and shares via React context.
3. Show a lightweight skeleton/loader while data is loading (for each section).
4. Update `Contact.jsx`:
   - Replace `localStorage` save with `POST /api/contact`.
   - Keep validation UX identical; toast on success/failure.
   - Remove `CONTACT_STORAGE_KEY` usage.
5. Keep `mock.js` around as a fallback/seed source but stop importing from components.

## Out of Scope (MVP)
- Auth / admin UI for viewing contact messages (GET /api/contact can be used in DevTools)
- File uploads (resume), emailing notifications
- Pagination / search on projects

## Testing
- Backend: deep_testing_backend_v2 — verify seed-on-first-call, GET /api/portfolio shape, POST /api/contact validation (empty, bad email, short message), successful submission, GET /api/contact list.
- Frontend: only after user approval.
