# DataScience

## BharatYatra Planner (Node.js)

A MakeMyTrip-style **Node.js** application focused on affordable travel and historic sites in India (bus/train/car), with NCERT/UPSC-oriented tagging.

### Features
- Pure Node.js backend (`http` module) with APIs:
  - `GET /api/sites`
  - `GET /api/meta`
  - `GET /api/notes/stream` (Server-Sent Events)
  - `POST /api/notes`
- Front-end filters for mode, budget, era, and state
- Broad NCERT/UPSC-oriented starter dataset in `data/historic-sites.json`
- Live collaborative planning notes via SSE (multi-user)

### Run locally
```bash
node server.js
```
Then open: `http://localhost:3000`

### Public cloud HTTP URL options (for simultaneous collaboration)
Because this environment blocks outbound tunnel/deploy connections, generate a public URL from your own machine using one of these:

```bash
# Option 1: localhost.run (no install)
ssh -R 80:localhost:3000 nokey@localhost.run

# Option 2: localtunnel
npx localtunnel --port 3000
```

### Important note on "all historic sites"
This app now contains a broad starter set aligned with common NCERT and UPSC art & architecture coverage.
For truly exhaustive coverage, keep appending records in:
- `data/historic-sites.json`
