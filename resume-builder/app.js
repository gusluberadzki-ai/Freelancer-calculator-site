// CONFIG
const PRO_URL = 'https://luberadzki.gumroad.com/l/resume-builder-pro';
const PRO_PRODUCT_ID = ''; // Gumroad product id, used only if licence keys are switched on for the product
// SHA-256 of the unlock code delivered to buyers on the Gumroad receipt
const UNLOCK_HASH = '63e08e140c3d601178b5346eb21108ba7f33f26fea751d6b5e529d576438ce92';

const $ = id => document.getElementById(id);
const store = {
  get(k, d) { try { const v = localStorage.getItem('rb-' + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem('rb-' + k, JSON.stringify(v)); } catch (e) {} }
};
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

const TEMPLATES = [
  { id: 'classic', name: 'Classic', pro: false },
  { id: 'modern', name: 'Modern', pro: true },
  { id: 'minimal', name: 'Minimal', pro: true },
  { id: 'executive', name: 'Executive', pro: true }
];
const COLORS = ['#0b6e4f', '#1f4e8c', '#7a2e8c', '#b03a2e', '#c27c0e', '#2b2b2b', '#127a8a'];

const SAMPLE = {
  name: 'Alex Morgan', title: 'Marketing Manager', email: 'alex.morgan@email.com', phone: '+44 7700 900123',
  loc: 'London, UK', web: 'linkedin.com/in/alexmorgan',
  summary: 'Marketing manager with 7 years of experience growing B2B software brands. I plan and run campaigns end to end, from strategy to reporting, and I love turning data into clear decisions.',
  exp: [
    { role: 'Marketing Manager', org: 'Brightline Software', dates: '2021 – Present', where: 'London',
      bullets: 'Grew inbound leads by 62% in 18 months with a new content and SEO plan\nManaged a £400k annual budget and a team of 4\nLaunched 3 products, each beating its first-quarter revenue target' },
    { role: 'Digital Marketing Executive', org: 'Northwind Agency', dates: '2018 – 2021', where: 'Manchester',
      bullets: 'Ran paid social for 12 clients, cutting cost per lead by 35%\nBuilt the agency\'s first email automation programme' }
  ],
  edu: [{ deg: 'BA (Hons) Business and Marketing', org: 'University of Leeds', dates: '2014 – 2017', info: 'First-class honours' }],
  skills: 'Content strategy, SEO, Google Ads, HubSpot, Email marketing, Data analysis, Team leadership, Copywriting',
  langs: 'English (native), French (B2)', certs: 'Google Ads Search Certification',
  clTo: 'Hiring Manager\nAcme Ltd',
  clBody: 'Dear Hiring Manager,\n\nI am writing to apply for the Head of Marketing role at Acme. Over the last seven years I have built marketing teams and programmes that turn interest into revenue, and I would love to bring that experience to you.\n\nAt Brightline Software I grew inbound leads by 62% in 18 months while managing a £400k budget. I am confident I can deliver similar results for Acme.\n\nThank you for your time. I look forward to hearing from you.\n\nKind regards,\nAlex Morgan'
};
const BLANK = { name: '', title: '', email: '', phone: '', loc: '', web: '', summary: '', exp: [{ role: '', org: '', dates: '', where: '', bullets: '' }], edu: [{ deg: '', org: '', dates: '', info: '' }], skills: '', langs: '', certs: '', clTo: '', clBody: '' };

let d = store.get('data', null) || JSON.parse(JSON.stringify(SAMPLE));
let tpl = store.get('tpl', 'classic');
let color = store.get('color', COLORS[0]);
let pro = store.get('pro', false);
let doc = 'cv';

const LISTS = {
  exp: { fields: [['role', 'Job title'], ['org', 'Company'], ['dates', 'Dates', '2021 – Present'], ['where', 'Location']], text: ['bullets', 'Achievements, one per line'] },
  edu: { fields: [['deg', 'Degree or course'], ['org', 'School'], ['dates', 'Dates'], ['info', 'Grade or note']] }
};

function drawLists() {
  for (const k of Object.keys(LISTS)) {
    const L = LISTS[k];
    $(k).innerHTML = d[k].map((e, i) => `<div class="entry">
      <div class="row"><button class="mini" type="button" data-mv="${k}:${i}:-1" aria-label="Move up">↑</button><button class="mini" type="button" data-mv="${k}:${i}:1" aria-label="Move down">↓</button><button class="mini" type="button" data-del="${k}:${i}">Remove</button></div>
      <div class="g2">${L.fields.map(([f, l, ph]) => `<div class="f"><label>${l}<input data-l="${k}:${i}:${f}" value="${esc(e[f])}" placeholder="${esc(ph || '')}"></label></div>`).join('')}</div>
      ${L.text ? `<label>${L.text[1]}<textarea data-l="${k}:${i}:${L.text[0]}">${esc(e[L.text[0]])}</textarea></label>` : ''}
    </div>`).join('');
  }
}

function drawPickers() {
  $('tpls').innerHTML = TEMPLATES.map(t => `<button type="button" data-tpl="${t.id}" class="${t.id === tpl ? 'on' : ''}">${t.name}<small>${t.pro ? (pro ? 'Pro' : 'Pro · preview') : 'Free'}</small></button>`).join('');
  $('sw').innerHTML = COLORS.map(c => `<button type="button" data-c="${c}" class="${c === color ? 'on' : ''}" style="background:${c}" aria-label="Colour ${c}"></button>`).join('');
}

const lines = s => String(s || '').split('\n').map(x => x.trim()).filter(Boolean);
const list = s => String(s || '').split(',').map(x => x.trim()).filter(Boolean);

function head(withContact = true) {
  const ct = [d.email, d.phone, d.loc, d.web].filter(Boolean).map(x => `<span>${esc(x)}</span>`).join('');
  return `<h1>${esc(d.name) || 'Your Name'}</h1>${d.title ? `<div class="jt">${esc(d.title)}</div>` : ''}${withContact && ct ? `<div class="ct">${ct}</div>` : ''}`;
}
function expHtml() {
  const jobs = d.exp.filter(e => e.role || e.org);
  if (!jobs.length) return '';
  return `<h2>Experience</h2>` + jobs.map(e => `<div class="job"><div class="jh"><div><b>${esc(e.role)}</b>${e.org ? `, ${esc(e.org)}` : ''}${e.where ? ` <span class="sub">· ${esc(e.where)}</span>` : ''}</div><div class="d">${esc(e.dates)}</div></div>
    ${lines(e.bullets).length ? `<ul>${lines(e.bullets).map(b => `<li>${esc(b.replace(/^[-•*]\s*/, ''))}</li>`).join('')}</ul>` : ''}</div>`).join('');
}
function eduHtml() {
  const ed = d.edu.filter(e => e.deg || e.org);
  if (!ed.length) return '';
  return `<h2>Education</h2>` + ed.map(e => `<div class="job"><div class="jh"><div><b>${esc(e.deg)}</b>${e.org ? `, ${esc(e.org)}` : ''}</div><div class="d">${esc(e.dates)}</div></div>${e.info ? `<div class="sub">${esc(e.info)}</div>` : ''}</div>`).join('');
}
function skillsHtml() {
  let h = list(d.skills).length ? `<h2>Skills</h2><div class="skills">${list(d.skills).map(s => `<span>${esc(s)}</span>`).join('')}</div>` : '';
  if (d.langs) h += `<h2>Languages</h2><p>${esc(d.langs)}</p>`;
  if (d.certs) h += `<h2>Certifications</h2><p>${esc(d.certs)}</p>`;
  return h;
}
const summaryHtml = () => d.summary ? `<h2>Profile</h2><p>${esc(d.summary)}</p>` : '';

function render() {
  const s = $('sheet');
  s.className = 'sheet ' + tpl; s.style.setProperty('--c', color);
  const wm = pro ? '' : '<div class="wm">Made with RateKit Resume Builder</div>';
  if (doc === 'cl') {
    s.className = 'sheet ' + (tpl === 'modern' ? 'classic' : tpl);
    s.innerHTML = `<div class="head">${head()}</div><div class="letter">${d.clTo ? `<div class="to">${esc(d.clTo)}</div>` : ''}${esc(d.clBody) || 'Write your cover letter on the left.'}</div>` + wm;
  } else if (tpl === 'modern') {
    const ct = [d.email, d.phone, d.loc, d.web].filter(Boolean).map(x => `<span>${esc(x)}</span>`).join('');
    s.innerHTML = `<div class="side">${head(false)}${ct ? `<h2>Contact</h2><div class="ct">${ct}</div>` : ''}${skillsHtml()}</div><div class="mainc">${summaryHtml()}${expHtml()}${eduHtml()}</div>` + wm;
  } else {
    s.innerHTML = `<div class="head">${head()}</div>${summaryHtml()}${expHtml()}${eduHtml()}${skillsHtml()}` + wm;
  }
  fit();
  store.set('data', d); store.set('tpl', tpl); store.set('color', color);
}

function fit() {
  const w = $('scaler').clientWidth, sc = Math.min(1, w / 794), s = $('sheet');
  s.style.transform = `scale(${sc})`;
  $('scaler').style.height = (s.offsetHeight * sc) + 'px';
}
window.addEventListener('resize', fit);

function say(html) { const m = $('msg'); m.innerHTML = html; m.style.display = html ? 'block' : 'none'; }

function needsPro() {
  if (pro) return '';
  const t = TEMPLATES.find(x => x.id === tpl);
  if (doc === 'cl') return 'The cover letter';
  if (t.pro) return `The ${t.name} template`;
  if (color !== COLORS[0]) return 'Custom colours';
  return '';
}

function setPro(on, viaPass) {
  pro = on; if (!viaPass) store.set('pro', on);
  $('proBox').style.display = on ? 'none' : '';
  drawPickers(); render();
}

// Unlocking
async function sha256(t) {
  const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(t));
  return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join('');
}
async function tryUnlock(raw) {
  const key = String(raw || '').trim(); if (!key) return false;
  $('keyMsg').textContent = 'Checking…';
  try { if (await sha256(key.toUpperCase()) === UNLOCK_HASH) { $('keyMsg').textContent = 'Pro unlocked. Thank you!'; setPro(true); return true; } } catch (e) {}
  if (PRO_PRODUCT_ID) {
    try {
      const r = await fetch('https://api.gumroad.com/v2/licenses/verify', { method: 'POST', body: new URLSearchParams({ product_id: PRO_PRODUCT_ID, license_key: key, increment_uses_count: 'false' }) });
      const j = await r.json();
      if (j.success && !j.purchase.refunded && !j.purchase.chargebacked) { $('keyMsg').textContent = 'Pro unlocked. Thank you!'; setPro(true); return true; }
    } catch (e) {}
  }
  if (window.RKPass && await RKPass.unlock(key)) { $('keyMsg').textContent = 'All-Access unlocked. Thank you!'; setPro(true, true); return true; }
  $('keyMsg').textContent = "That code wasn't recognised. Check it and try again.";
  return false;
}

// Init
$('buyPro').href = PRO_URL;
document.querySelectorAll('[data-f]').forEach(el => { el.value = d[el.dataset.f] || ''; });
drawLists(); drawPickers(); setPro(pro);

// RateKit All-Access membership (pro/pass.js) also unlocks Pro, without touching the one-off purchase flag.
if (window.RKPass) {
  const own = () => !!store.get('pro', false);
  if (!own() && RKPass.active()) setPro(true, true);
  RKPass.fromHash().then(() => RKPass.verify()).then(ok => { if (!own()) setPro(ok, true); });
}
function hashUnlock() {
  const hm = location.hash.match(/unlock=([\w-]+)/);
  if (hm) tryUnlock(decodeURIComponent(hm[1])).then(ok => { if (ok) say('Pro is unlocked on this device. Bookmark this page link to unlock it on other devices too.'); });
}
hashUnlock(); window.addEventListener('hashchange', hashUnlock);

document.addEventListener('input', e => {
  const t = e.target;
  if (t.dataset.f) { d[t.dataset.f] = t.value; render(); }
  else if (t.dataset.l) { const [k, i, f] = t.dataset.l.split(':'); d[k][+i][f] = t.value; render(); }
});
document.addEventListener('click', e => {
  const t = e.target.closest('button'); if (!t) return;
  if (t.dataset.add) { d[t.dataset.add].push(JSON.parse(JSON.stringify(BLANK[t.dataset.add][0]))); drawLists(); render(); }
  if (t.dataset.del) { const [k, i] = t.dataset.del.split(':'); d[k].splice(+i, 1); drawLists(); render(); }
  if (t.dataset.mv) {
    const [k, i, dir] = t.dataset.mv.split(':'); const a = +i, b = a + +dir;
    if (b >= 0 && b < d[k].length) { [d[k][a], d[k][b]] = [d[k][b], d[k][a]]; drawLists(); render(); }
  }
  if (t.dataset.tpl) { tpl = t.dataset.tpl; drawPickers(); render(); say(''); }
  if (t.dataset.c) { color = t.dataset.c; drawPickers(); render(); say(''); }
  if (t.dataset.doc) { doc = t.dataset.doc; document.querySelectorAll('[data-doc]').forEach(b => b.classList.toggle('on', b === t)); render(); say(''); }
});
$('key').onchange = () => tryUnlock($('key').value);
$('pdf').onclick = () => {
  const why = needsPro();
  if (why) { say(`${esc(why)} is part of Pro. <a href="${PRO_URL}" target="_blank" rel="noopener">Get Pro for CHF 7</a>, or switch to the free Classic template in green to download for free.`); return; }
  say('');
  const old = document.title; document.title = ((d.name || 'resume') + (doc === 'cl' ? ' cover letter' : ' resume')).replace(/[^\w-]+/g, '_');
  window.print(); document.title = old;
};
$('export').onclick = () => {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify({ d, tpl, color }, null, 2)], { type: 'application/json' }));
  a.download = 'my-resume.json'; a.click();
};
$('import').onchange = e => {
  const f = e.target.files[0]; if (!f) return;
  f.text().then(t => { const j = JSON.parse(t); d = Object.assign(JSON.parse(JSON.stringify(BLANK)), j.d || j); tpl = j.tpl || tpl; color = j.color || color;
    document.querySelectorAll('[data-f]').forEach(el => { el.value = d[el.dataset.f] || ''; }); drawLists(); drawPickers(); render(); }).catch(() => say("That file couldn't be read."));
};
$('clear').onclick = () => { d = JSON.parse(JSON.stringify(BLANK)); document.querySelectorAll('[data-f]').forEach(el => { el.value = ''; }); drawLists(); render(); };
