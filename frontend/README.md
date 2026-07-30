# Assessment Automation — Frontend

React 19 + Vite + React Query. See the top-level [README](../README.md) for the full project overview.

## Scripts

```bash
npm install     # once
npm run dev     # dev server on http://localhost:5173, proxies /api to VITE_BACKEND_URL (default http://localhost:8000)
npm run build   # production build → dist/
npm run preview # serve the production build locally
npm run lint    # oxlint
```

## Environment

- `VITE_BACKEND_URL` — dev-only; sets the proxy target for `/api`, `/uploads`, `/static`, `/downloads`.
- `VITE_API_BASE_URL` — used at runtime; defaults to `/api`. Override for cross-origin setups.

## Layout

```
src/
    main.jsx                 # React root, providers (QueryClient, BrowserRouter, Toaster)
    App.jsx                  # route table
    AppShell.jsx             # sidebar + topbar layout
    lib/                     # http, api client, query client, format, constants
    hooks/                   # React Query wrappers grouped by domain
    components/ui/           # design-token primitives
    components/assessment/   # AssessmentToolbar, SubmissionPanel
    components/question/     # QuestionCard
    pages/                   # one file per route
    styles/                  # tokens + base css
```

All CSS is plain (no framework). Design tokens live in `styles/tokens.css` and every component references them via `var(--...)`.
