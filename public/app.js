const stateSelect = document.getElementById('state');
const cards = document.getElementById('cards');
const summary = document.getElementById('summary');
const notes = document.getElementById('notes');

function currency(v) {
  return new Intl.NumberFormat('en-IN', { maximumFractionDigits: 0 }).format(v);
}

async function loadMeta() {
  const meta = await fetch('/api/meta').then((r) => r.json());
  stateSelect.innerHTML = '<option value="all">All states</option>' + meta.states.map((s) => `<option value="${s}">${s}</option>`).join('');
}

function buildQuery() {
  const params = new URLSearchParams();
  ['q', 'mode', 'budgetTier', 'era', 'state'].forEach((id) => {
    const value = document.getElementById(id).value;
    if (value) params.set(id, value);
  });
  return params.toString();
}

async function loadSites() {
  const query = buildQuery();
  const data = await fetch(`/api/sites?${query}`).then((r) => r.json());
  summary.textContent = `${data.count} sites found`;

  cards.innerHTML = data.sites.map((s) => `
    <article class="bg-white p-4 rounded-xl shadow border border-slate-200">
      <h3 class="font-bold text-lg">${s.name}</h3>
      <p class="text-sm mt-1">${s.city}, ${s.state}</p>
      <p class="text-sm mt-1"><strong>Era:</strong> ${s.era}</p>
      <p class="text-sm mt-1"><strong>Type:</strong> ${s.type}</p>
      <p class="text-sm mt-1"><strong>Reference:</strong> ${s.ncertUpscTag}</p>
      <p class="text-sm mt-1"><strong>Budget:</strong> ${s.budgetTier.toUpperCase()} (₹${currency(s.avgTripCost)})</p>
      <div class="mt-2 flex gap-2 flex-wrap">
        ${s.transport.map((t) => `<span class="text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded-full">${t}</span>`).join('')}
      </div>
    </article>
  `).join('');

  if (!data.sites.length) {
    cards.innerHTML = '<div class="bg-white rounded p-4 border">No results. Try changing filters.</div>';
  }
}

document.getElementById('apply').addEventListener('click', loadSites);

document.getElementById('sendNote').addEventListener('click', async () => {
  const input = document.getElementById('noteInput');
  const message = input.value.trim();
  if (!message) return;

  await fetch('/api/notes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });

  input.value = '';
});

const eventSource = new EventSource('/api/notes/stream');
eventSource.addEventListener('note', (event) => {
  const { message, at } = JSON.parse(event.data);
  const li = document.createElement('li');
  li.className = 'bg-slate-100 p-2 rounded';
  li.textContent = `${new Date(at).toLocaleTimeString()} - ${message}`;
  notes.prepend(li);
});

loadMeta().then(loadSites);
