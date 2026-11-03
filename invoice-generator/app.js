// CONFIG: fill these in once the Pro product exists on Gumroad.
const PRO_URL = 'https://luberadzki.gumroad.com/l/ratekit-pro';
const PRO_PRODUCT_ID = '02vclgFQ_PI3U5MZhZV6Jw==';

const $ = id => document.getElementById(id);
const FIELDS = ['from', 'to', 'num', 'cur', 'date', 'due', 'tax', 'disc', 'notes', 'brand'];
const ls = {
  get(k, d) { try { const v = localStorage.getItem('ik-' + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem('ik-' + k, JSON.stringify(v)); } catch (e) {} }
};
let items = ls.get('items', [{ d: 'Website design', q: 1, p: 1800 }, { d: 'Hosting setup', q: 2, p: 75 }]);
let logo = ls.get('logo', '');
let pro = ls.get('pro', false);

const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const money = n => { try { return new Intl.NumberFormat(undefined, { style: 'currency', currency: $('cur').value }).format(n || 0); } catch (e) { return (n || 0).toFixed(2); } };
const iso = d => d.toISOString().slice(0, 10);
const nice = s => s ? new Date(s + 'T00:00').toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' }) : '';

function drawItems() {
  $('items').innerHTML = items.map((it, i) => `<div class="item">
    <input data-i="${i}" data-k="d" value="${esc(it.d)}" placeholder="Description">
    <input data-i="${i}" data-k="q" type="number" step="any" value="${it.q}">
    <input data-i="${i}" data-k="p" type="number" step="any" value="${it.p}">
    <button type="button" data-del="${i}" aria-label="Remove item">×</button></div>`).join('');
}

function render() {
  const v = {}; FIELDS.forEach(f => v[f] = $(f).value);
  const sub = items.reduce((s, it) => s + (parseFloat(it.q) || 0) * (parseFloat(it.p) || 0), 0);
  const disc = parseFloat(v.disc) || 0, tax = (sub - disc) * (parseFloat(v.tax) || 0) / 100;
  $('inv').style.setProperty('--brand', v.brand);
  $('inv').innerHTML = `
    <div class="top"><div>${logo ? `<img class="logo" src="${logo}" alt="">` : ''}<h2>INVOICE</h2></div>
      <div class="meta"><strong>${esc(v.num)}</strong><br>Issued ${nice(v.date)}<br>Due ${nice(v.due)}</div></div>
    <div class="parties"><div><div class="lbl">From</div>${esc(v.from)}</div><div><div class="lbl">Bill to</div>${esc(v.to)}</div></div>
    <table><tr><th>Description</th><th>Qty</th><th>Price</th><th>Amount</th></tr>
      ${items.map(it => `<tr><td>${esc(it.d)}</td><td>${esc(it.q)}</td><td>${money(parseFloat(it.p))}</td><td>${money((parseFloat(it.q) || 0) * (parseFloat(it.p) || 0))}</td></tr>`).join('')}</table>
    <div class="totals"><div><span>Subtotal</span><span>${money(sub)}</span></div>
      ${disc ? `<div><span>Discount</span><span>−${money(disc)}</span></div>` : ''}
      ${parseFloat(v.tax) ? `<div><span>Tax (${esc(v.tax)}%)</span><span>${money(tax)}</span></div>` : ''}
      <div class="grand"><span>Total due</span><span>${money(sub - disc + tax)}</span></div></div>
    ${v.notes ? `<div class="notes"><div class="lbl">Notes</div>${esc(v.notes)}</div>` : ''}
    ${pro ? '' : '<div class="brandline">Made with RateKit, the free invoice generator</div>'}`;
  FIELDS.forEach(f => ls.set(f, $(f).value)); ls.set('items', items);
}

function setPro(on) {
  pro = on; ls.set('pro', on);
  $('proBox').style.display = on ? 'none' : '';
  $('proTools').style.display = on ? '' : 'none';
  drawClients(); render();
}

function drawClients() {
  const cs = ls.get('clients', []);
  $('clients').innerHTML = '<option value="">Load a saved client…</option>' + cs.map((c, i) => `<option value="${i}">${esc(c.split('\n')[0])}</option>`).join('');
}

// Init
const today = new Date(), due = new Date(); due.setDate(due.getDate() + 14);
FIELDS.forEach(f => { const s = ls.get(f, null); if (s !== null) $(f).value = s; });
if (!$('date').value) $('date').value = iso(today);
if (!$('due').value) $('due').value = iso(due);
if (PRO_URL) $('buyPro').href = PRO_URL; else { $('buyPro').textContent = 'Coming soon'; $('buyPro').removeAttribute('href'); }
drawItems(); setPro(pro);

document.addEventListener('input', e => {
  const t = e.target;
  if (t.dataset.k) { items[t.dataset.i][t.dataset.k] = t.dataset.k === 'd' ? t.value : t.value; }
  if (t.id !== 'key' && t.id !== 'logo') render();
});
$('items').addEventListener('click', e => { if (e.target.dataset.del !== undefined) { items.splice(+e.target.dataset.del, 1); drawItems(); render(); } });
$('add').onclick = () => { items.push({ d: '', q: 1, p: 0 }); drawItems(); render(); };
$('logo').onchange = e => {
  const f = e.target.files[0]; if (!f) return;
  const r = new FileReader(); r.onload = () => { logo = r.result; ls.set('logo', logo); render(); }; r.readAsDataURL(f);
};
$('pdf').onclick = () => {
  const old = document.title; document.title = ($('num').value || 'invoice').replace(/[^\w-]+/g, '_');
  window.print(); document.title = old;
  if (pro) { // auto-number the next invoice
    const m = $('num').value.match(/^(.*?)(\d+)$/);
    if (m) ls.set('nextNum', m[1] + String(+m[2] + 1).padStart(m[2].length, '0'));
  }
};
$('reset').onclick = () => {
  items = [{ d: '', q: 1, p: 0 }]; $('to').value = ''; $('date').value = iso(new Date());
  const d2 = new Date(); d2.setDate(d2.getDate() + 14); $('due').value = iso(d2);
  const n = ls.get('nextNum', null); if (pro && n) $('num').value = n;
  drawItems(); render();
};
$('saveClient').onclick = () => { const cs = ls.get('clients', []); if ($('to').value.trim()) { cs.push($('to').value); ls.set('clients', cs); drawClients(); } };
$('clients').onchange = e => { if (e.target.value !== '') { $('to').value = ls.get('clients', [])[+e.target.value]; render(); } };
$('key').onchange = async () => {
  const key = $('key').value.trim(); if (!key) return;
  if (!PRO_PRODUCT_ID) { $('keyMsg').textContent = 'Pro is not on sale yet.'; return; }
  $('keyMsg').textContent = 'Checking…';
  try {
    const r = await fetch('https://api.gumroad.com/v2/licenses/verify', {
      method: 'POST', body: new URLSearchParams({ product_id: PRO_PRODUCT_ID, license_key: key, increment_uses_count: 'false' })
    });
    const j = await r.json();
    if (j.success && !j.purchase.refunded && !j.purchase.chargebacked) { $('keyMsg').textContent = 'Pro unlocked. Thank you!'; setPro(true); }
    else $('keyMsg').textContent = "That key wasn't recognised. Check it and try again.";
  } catch (e) { $('keyMsg').textContent = "Couldn't reach the licence server. Try again in a moment."; }
};
