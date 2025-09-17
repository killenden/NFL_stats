// Theme toggle: inserts a button into the nav, persists choice in localStorage,
// and sets documentElement.dataset.theme = 'light'|'dark' when user selects.
(function(){
  const STORAGE_KEY = 'nflstats-theme';

  function systemPrefersDark(){
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }

  function applyTheme(theme){
    if(theme) document.documentElement.dataset.theme = theme;
    else delete document.documentElement.dataset.theme;
    updateButton(theme);
    // debug: report applied theme and resolved nav colors
    try{
      const computed = getComputedStyle(document.documentElement);
      console.debug('theme-toggle: applied theme=', theme, 'dataset=', document.documentElement.dataset.theme, 'nav-bg=', computed.getPropertyValue('--nav-bg').trim(), 'nav-link-color=', computed.getPropertyValue('--nav-link-color').trim());
    }catch(e){ console.debug('theme-toggle debug error', e); }
  }

  function updateButton(theme){
    const btn = document.getElementById('theme-toggle-btn');
    if(!btn) return;
    const current = theme ?? document.documentElement.dataset.theme ?? (systemPrefersDark() ? 'dark' : 'light');
    btn.textContent = current === 'dark' ? '🌙 Dark' : '🌤️ Light';
    btn.setAttribute('aria-pressed', current === 'dark');
  }

  function toggle(){
    const stored = localStorage.getItem(STORAGE_KEY);
    let next;
    if(stored === 'dark') next = 'light';
    else if(stored === 'light') next = null; // cycle back to system
    else {
      // no stored preference -> pick opposite of system
      next = systemPrefersDark() ? 'light' : 'dark';
    }
    if(next) localStorage.setItem(STORAGE_KEY, next); else localStorage.removeItem(STORAGE_KEY);
    applyTheme(next);
  }

  function init(){
    // create button and insert into nav
    const nav = document.querySelector('nav');
    if(!nav) return;
    const btn = document.createElement('button');
    btn.id = 'theme-toggle-btn';
    btn.className = 'block-toggle';
    btn.style.marginLeft = '10px';
    btn.style.verticalAlign = 'middle';
    btn.title = 'Toggle theme (cycles: dark → light → system)';
    btn.onclick = toggle;
    nav.appendChild(btn);

    // initialize theme from localStorage or system
    const stored = localStorage.getItem(STORAGE_KEY);
    if(stored === 'dark' || stored === 'light') applyTheme(stored);
    else applyTheme(null);

    // listen for system changes when no stored preference
    if(window.matchMedia){
      const mq = window.matchMedia('(prefers-color-scheme: dark)');
      mq.addEventListener ? mq.addEventListener('change', () => {
        if(!localStorage.getItem(STORAGE_KEY)) applyTheme(null);
      }) : mq.addListener(() => { if(!localStorage.getItem(STORAGE_KEY)) applyTheme(null); });
    }
  }

  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
