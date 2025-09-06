// assets/js/script.js
(() => {
  // Prevent double init if script gets included twice
  if (window.__mtv2_init_done) return;
  window.__mtv2_init_done = true;

  const run = () => {
    initNavbarScrollEffect();
    highlightCurrentNavLink();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run, { once: true });
  } else {
    run();
  }

  // --- Navbar scroll background toggle ---
  function initNavbarScrollEffect() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    const getTrigger = () => Math.round(window.innerHeight * 0.15);
    let trigger = getTrigger();

    const setSolid = (on) => {
      navbar.classList.toggle('navbar-solid', on);
      navbar.classList.toggle('navbar-transparent', !on);
    };

    const update = () => setSolid(window.scrollY > trigger);

    update();
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', () => { trigger = getTrigger(); update(); }, { passive: true });
    window.addEventListener('orientationchange', () => { trigger = getTrigger(); update(); }, { passive: true });
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'visible') update();
    });
  }

  // --- Current nav link highlight (Django URLs) ---
  function highlightCurrentNavLink() {
    const links = document.querySelectorAll('.nav-link[href]');
    if (!links.length) return;

    const current = normalisePath(location.pathname);

    links.forEach(link => {
      const href = link.getAttribute('href') || '';

      // Ignore non-page links
      if (
        href === '' ||
        href.startsWith('#') ||
        href.startsWith('mailto:') ||
        href.startsWith('tel:') ||
        /^https?:\/\//i.test(href)
      ) {
        link.classList.remove('active');
        return;
      }

      const a = document.createElement('a');
      a.href = href;
      const linkPath = normalisePath(a.pathname || '/');
      link.classList.toggle('active', linkPath === current);
    });

    function normalisePath(p) {
      if (!p) return '/';
      if (!p.endsWith('/')) p += '/';
      return p.replace(/\/{2,}/g, '/');
    }
  }
})();

