const http = require("http");
const fs = require("fs");
const path = require("path");
const { URL } = require("url");
const historicSites = require("./data/historicSites");

const PORT = process.env.PORT || 3000;

const transportCostsPerKm = { bus: 1.2, train: 0.9, car: 6.5 };

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function renderHomePage(query) {
  const state = query.get("state") || "";
  const mode = query.get("mode") || "";
  const maxBudget = query.get("maxBudget") || "";
  const q = query.get("q") || "";

  const filteredSites = historicSites.filter((site) => {
    const stateMatch = !state || site.state.toLowerCase() === state.toLowerCase();
    const keyword = q.trim().toLowerCase();
    const keywordMatch =
      !keyword ||
      site.name.toLowerCase().includes(keyword) ||
      site.era.toLowerCase().includes(keyword) ||
      site.category.toLowerCase().includes(keyword);
    return stateMatch && keywordMatch;
  });

  const estimatedDistanceKm = 250;
  const costPerKm = transportCostsPerKm[mode] || 0;
  const estimatedTravelCost = costPerKm * estimatedDistanceKm;

  const budgetAdvice =
    mode && maxBudget
      ? estimatedTravelCost <= Number(maxBudget)
        ? `Great! A typical ${mode} route (~${estimatedDistanceKm} km) is within your budget.`
        : `Budget may be tight for ${mode}. Try train/bus combo or overnight sleeper options.`
      : "Select transport mode and budget to get affordability advice.";

  const states = [...new Set(historicSites.map((site) => site.state))].sort();

  const options = states
    .map(
      (s) =>
        `<option value="${escapeHtml(s)}" ${state === s ? "selected" : ""}>${escapeHtml(
          s
        )}</option>`
    )
    .join("");

  const cards = filteredSites
    .map(
      (site) => `
      <article class="site-card">
        <h2>${escapeHtml(site.name)}</h2>
        <p><strong>State:</strong> ${escapeHtml(site.state)}</p>
        <p><strong>Era:</strong> ${escapeHtml(site.era)}</p>
        <p><strong>Category:</strong> ${escapeHtml(site.category)}</p>
        <p><strong>Why it matters:</strong> ${escapeHtml(site.significance)}</p>
        <p><strong>Nearest Rail:</strong> ${escapeHtml(site.nearestRail)}</p>
        <p><strong>Nearest Airport:</strong> ${escapeHtml(site.nearestAirport)}</p>
        <p><strong>Budget Tip:</strong> ${escapeHtml(site.budgetHint)}</p>
      </article>
    `
    )
    .join("");

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>India Heritage Travel Planner</title>
  <link rel="stylesheet" href="/styles.css" />
</head>
<body>
  <header>
    <h1>India Heritage Travel Planner</h1>
    <p>Explore NCERT/UPSC art-architecture aligned historic destinations with affordable bus, train, and car planning.</p>
    <p class="small-note">Current curated list: <strong>${historicSites.length}</strong> major exam-relevant historic sites across India.</p>
  </header>

  <section class="filters">
    <form method="GET" action="/">
      <div>
        <label for="state">State</label>
        <select id="state" name="state">
          <option value="">All States</option>
          ${options}
        </select>
      </div>
      <div>
        <label for="mode">Travel Mode</label>
        <select id="mode" name="mode">
          <option value="">Select Mode</option>
          <option value="bus" ${mode === "bus" ? "selected" : ""}>Bus</option>
          <option value="train" ${mode === "train" ? "selected" : ""}>Train</option>
          <option value="car" ${mode === "car" ? "selected" : ""}>Car</option>
        </select>
      </div>
      <div>
        <label for="maxBudget">Max Budget (INR)</label>
        <input id="maxBudget" name="maxBudget" type="number" min="0" value="${escapeHtml(maxBudget)}" />
      </div>
      <div>
        <label for="q">Search</label>
        <input id="q" name="q" type="text" placeholder="e.g. Mughal, Chola, Buddhist" value="${escapeHtml(q)}" />
      </div>
      <button type="submit">Apply Filters</button>
    </form>

    <div class="budget-box">
      <p><strong>Affordability Insight:</strong> ${escapeHtml(budgetAdvice)}</p>
      ${estimatedTravelCost ? `<p>Estimated 250 km one-way cost: ₹${estimatedTravelCost.toFixed(0)}</p>` : ""}
    </div>
  </section>

  <main>
    ${filteredSites.length ? `<div class="card-grid">${cards}</div>` : "<p>No sites found for current filters.</p>"}
  </main>
</body>
</html>`;
}

const server = http.createServer((req, res) => {
  const parsedUrl = new URL(req.url, `http://${req.headers.host}`);

  if (parsedUrl.pathname === "/styles.css") {
    const cssPath = path.join(__dirname, "public", "styles.css");
    const css = fs.readFileSync(cssPath, "utf8");
    res.writeHead(200, { "Content-Type": "text/css" });
    res.end(css);
    return;
  }

  if (parsedUrl.pathname === "/api/sites") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ count: historicSites.length, sites: historicSites }, null, 2));
    return;
  }

  if (parsedUrl.pathname === "/") {
    res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
    res.end(renderHomePage(parsedUrl.searchParams));
    return;
  }

  res.writeHead(404, { "Content-Type": "text/plain" });
  res.end("Not Found");
});

server.listen(PORT, () => {
  console.log(`India Heritage Travel app running on http://localhost:${PORT}`);
});
