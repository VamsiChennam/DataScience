# India Heritage Travel Planner (Node.js)

A MakeMyTrip-style starter web app for affordable travel planning across major Indian historic sites often referenced in NCERT and UPSC art & architecture prep.

## Features
- Browse curated historic sites by state, era, and category.
- Filter by transport mode (bus/train/car) and budget.
- See nearby rail/airport hubs and cost-saving hints.
- JSON API endpoint at `/api/sites`.

## Run locally
```bash
cd india-travel-app
npm install
npm start
```
Then open `http://localhost:3000`.

## Deploy to cloud and get public URL
You can deploy quickly on:
1. **Render** (free tier): create a Web Service, build command `npm install`, start command `npm start`.
2. **Railway**: `railway up` after connecting GitHub repo.
3. **Fly.io**: `fly launch` then `fly deploy`.

After deployment, you get a public `https://...` URL that you can keep enhancing through Git pushes.

## Notes on historical coverage
This app includes a broad exam-focused starter dataset. Since NCERT and UPSC references span many books and evolving lists, you can keep extending `data/historicSites.js` to include additional sites chapter-wise.
