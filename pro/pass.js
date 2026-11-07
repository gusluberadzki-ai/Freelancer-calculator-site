// RateKit All-Access pass, shared by every RateKit app on this site.
// Two ways to unlock:
//  1. Unlock code from the membership receipt / monthly member email (#unlock=AA-XXXX).
//     Valid codes are listed as SHA-256 hashes below. Rotate monthly: add the new hash, drop codes older than ~2 months.
//  2. Gumroad licence key (if licence keys are switched on for the membership). The subscription status is
//     re-checked with Gumroad every 7 days, so cancelled members lose access automatically.
(function () {
  const CFG = {
    BUY_URL: 'https://luberadzki.gumroad.com/l/all-access',
    PRODUCT_ID: '0qkVfrEj_6xFP5jmYQyifg==',
    CODE_HASHES: ['d02fc7d857ce270f9570a1b07bb5e406b6f70dcd80d0f5114c5fac2a133f18ff'],
    RECHECK_MS: 7 * 864e5
  };
  const KEY = 'rk-pass';
  const read = () => { try { return JSON.parse(localStorage.getItem(KEY)) || null; } catch (e) { return null; } };
  const write = v => { try { v ? localStorage.setItem(KEY, JSON.stringify(v)) : localStorage.removeItem(KEY); } catch (e) {} };
  async function sha256(t) {
    const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(t));
    return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join('');
  }
  async function checkKey(key) {
    const r = await fetch('https://api.gumroad.com/v2/licenses/verify', {
      method: 'POST', body: new URLSearchParams({ product_id: CFG.PRODUCT_ID, license_key: key, increment_uses_count: 'false' })
    });
    const j = await r.json();
    const p = j.purchase || {};
    return !!(j.success && !p.refunded && !p.chargebacked && !p.subscription_ended_at && !p.subscription_failed_at);
  }
  async function unlock(raw) {
    const code = String(raw || '').trim(); if (!code) return false;
    if (CFG.CODE_HASHES.includes(await sha256(code.toUpperCase()))) { write({ via: 'code', code: code.toUpperCase(), at: Date.now() }); return true; }
    try { if (await checkKey(code)) { write({ via: 'key', code, at: Date.now() }); return true; } } catch (e) {}
    return false;
  }
  // Synchronous best guess for page start-up; verify() confirms in the background.
  function active() { const p = read(); return !!p; }
  async function verify() {
    const p = read(); if (!p) return false;
    if (p.via === 'code') { const ok = CFG.CODE_HASHES.includes(await sha256(p.code)); if (!ok) write(null); return ok; }
    if (Date.now() - p.at < CFG.RECHECK_MS) return true;
    try { const ok = await checkKey(p.code); if (ok) { p.at = Date.now(); write(p); } else write(null); return ok; }
    catch (e) { return true; } // offline: keep access until we can check
  }
  async function fromHash() {
    const m = location.hash.match(/unlock=([\w-]+)/);
    if (!m) return null;
    const ok = await unlock(decodeURIComponent(m[1]));
    if (ok) history.replaceState(null, '', location.pathname + location.search);
    return ok;
  }
  window.RKPass = { CFG, active, verify, unlock, fromHash, clear: () => write(null) };
})();
