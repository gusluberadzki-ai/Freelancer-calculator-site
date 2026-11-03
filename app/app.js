// Storage: chrome.storage.local in the extension, localStorage when opened as a plain page (for testing).
const store = (typeof chrome !== 'undefined' && chrome.storage && chrome.storage.local)
  ? { get: () => chrome.storage.local.get('tb').then(r => r.tb), set: v => chrome.storage.local.set({ tb: v }) }
  : { get: async () => JSON.parse(localStorage.getItem('tb') || 'null'), set: async v => localStorage.setItem('tb', JSON.stringify(v)) };

let S = { clients: [{ id: 'c1', name: 'My first client', rate: 50 }], entries: [], running: null, currency: 'USD' };
const $ = id => document.getElementById(id);
const save = () => store.set(S);

const money = n => new Intl.NumberFormat(undefined, { style: 'currency', currency: S.currency, maximumFractionDigits: 0 }).format(n || 0);
const hms = ms => { const s = Math.floor(ms / 1000); return `${Math.floor(s / 3600)}:${String(Math.floor(s / 60) % 60).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`; };
const hrs = ms => (ms / 3600000);
const client = id => S.clients.find(c => c.id === id) || { name: 'Deleted client', rate: 0 };
const weekStart = () => { const d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() - ((d.getDay() + 6) % 7)); return d.getTime(); };

function render() {
  const sel = $('client'), cur = S.running ? S.running.client : sel.value;
  sel.innerHTML = S.clients.map(c => `<option value="${c.id}">${esc(c.name)} · ${money(c.rate)}/h</option>`).join('');
  if (cur && S.clients.some(c => c.id === cur)) sel.value = cur;
  sel.disabled = !!S.running;
  $('toggle').textContent = S.running ? 'Stop' : 'Start';
  $('toggle').classList.toggle('stop', !!S.running);
  if (S.running) $('note').value = S.running.note || '';

  const ws = weekStart(), per = {};
  S.entries.filter(e => e.start >= ws).forEach(e => { per[e.client] = (per[e.client] || 0) + (e.end - e.start); });
  let totalMs = 0, totalEarn = 0;
  $('summary').innerHTML = Object.entries(per).map(([id, ms]) => {
    const c = client(id), earn = hrs(ms) * c.rate; totalMs += ms; totalEarn += earn;
    return `<tr><td>${esc(c.name)}</td><td>${hrs(ms).toFixed(2)} h</td><td>${money(earn)}</td></tr>`;
  }).join('') || '<tr><td class="small">No time tracked this week yet.</td></tr>';
  $('weekEarn').textContent = totalMs ? money(totalEarn) : '';
  $('weekTotal').textContent = totalMs ? `${hrs(totalMs).toFixed(1)} h this week` : '';

  $('recent').innerHTML = S.entries.slice(-5).reverse().map(e =>
    `<tr><td>${esc(client(e.client).name)}<div class="small">${esc(e.note || '')}</div></td><td>${new Date(e.start).toLocaleDateString()}</td><td>${hms(e.end - e.start)}</td></tr>`).join('');
  tick();
}

function tick() {
  if (!S.running) { $('clock').textContent = '0:00:00'; $('liveEarn').innerHTML = '&nbsp;'; return; }
  const ms = Date.now() - S.running.start;
  $('clock').textContent = hms(ms);
  $('liveEarn').textContent = money(hrs(ms) * client(S.running.client).rate) + ' earned';
}

function badge(on) {
  if (typeof chrome !== 'undefined' && chrome.action) {
    chrome.action.setBadgeText({ text: on ? '●' : '' });
    chrome.action.setBadgeBackgroundColor({ color: '#c0392b' });
  }
}

const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

$('toggle').onclick = () => {
  if (S.running) {
    S.entries.push({ ...S.running, note: $('note').value, end: Date.now() });
    S.running = null; $('note').value = ''; badge(false);
  } else {
    if (!S.clients.length) return;
    S.running = { client: $('client').value, start: Date.now(), note: $('note').value }; badge(true);
  }
  save(); render();
};
$('note').oninput = () => { if (S.running) { S.running.note = $('note').value; save(); } };
$('showAdd').onclick = () => { const f = $('addForm'); f.style.display = f.style.display === 'block' ? 'none' : 'block'; $('newName').focus(); };
$('addBtn').onclick = () => {
  const name = $('newName').value.trim(), rate = parseFloat($('newRate').value) || 0;
  if (!name) return;
  S.clients.push({ id: 'c' + Date.now(), name, rate });
  $('newName').value = $('newRate').value = ''; $('addForm').style.display = 'none';
  save(); render(); $('client').value = S.clients[S.clients.length - 1].id;
};
$('export').onclick = () => {
  const rows = [['Client', 'Date', 'Start', 'End', 'Hours', 'Rate', 'Amount', 'Note']].concat(S.entries.map(e => {
    const c = client(e.client), s = new Date(e.start), en = new Date(e.end), h = hrs(e.end - e.start);
    return [c.name, s.toLocaleDateString(), s.toLocaleTimeString(), en.toLocaleTimeString(), h.toFixed(2), c.rate, (h * c.rate).toFixed(2), e.note || ''];
  }));
  const csv = rows.map(r => r.map(x => `"${String(x).replace(/"/g, '""')}"`).join(',')).join('\n');
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }));
  a.download = `timesheet-${new Date().toISOString().slice(0, 10)}.csv`; a.click();
};
$('currency').onchange = () => { S.currency = $('currency').value; save(); render(); };
let armed = false;
$('clearAll').onclick = () => {
  if (!armed) { armed = true; $('clearAll').textContent = 'Click again to delete all'; setTimeout(() => { armed = false; $('clearAll').textContent = 'Reset'; }, 3000); return; }
  S = { clients: [], entries: [], running: null, currency: S.currency }; badge(false); save(); render();
};

store.get().then(v => {
  if (v) S = v;
  $('currency').value = S.currency;
  render(); setInterval(tick, 1000);
});
