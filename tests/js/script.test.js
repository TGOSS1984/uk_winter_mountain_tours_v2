// tests/js/script.test.js
// Import (require) the IIFE file to execute it per test.
// It guards against double-init via window.__mtv2_init_done, so must reset modules and clear that flag.
/** @jest-environment jsdom */

function loadScript() {
  // ensure a fresh module instance per test
  jest.resetModules();
  delete window.__mtv2_init_done;

  // JSDOM defaults 'loading' sometimes; force a known state so run() fires immediately
  Object.defineProperty(document, 'readyState', { value: 'complete', configurable: true });

  // Import AFTER prepare DOM/window so the IIFE runs with setup
  require('../../assets/js/script.js'); 
}

describe('script.js IIFE behaviours', () => {
  beforeEach(() => {
    // Minimal DOM skeleton used by the script
    document.body.innerHTML = `
      <nav id="navbar" class="navbar-transparent"></nav>

      <a class="nav-link" href="/"></a>
      <a class="nav-link" href="/about"></a>
      <a class="nav-link" href="https://example.com"></a>
      <a class="nav-link" href="#contact"></a>
      <a class="nav-link" href="mailto:test@example.com"></a>
    `;

    // Make viewport + scroll controllable
    Object.defineProperty(window, 'innerHeight', { value: 1000, writable: true }); // trigger = 150
    Object.defineProperty(window, 'scrollY', { value: 0, writable: true });

    // Set current path to /about/ so highlight matches the /about link
    window.history.pushState({}, '', '/about/');
  });

  test('navbar toggles transparent/solid based on scroll threshold (~15% vh)', () => {
    loadScript();

    const navbar = document.getElementById('navbar');
    // initial state at scrollY=0 -> transparent
    expect(navbar.classList.contains('navbar-transparent')).toBe(true);
    expect(navbar.classList.contains('navbar-solid')).toBe(false);

    // Scroll past trigger (150)
    window.scrollY = 200;
    window.dispatchEvent(new Event('scroll'));

    expect(navbar.classList.contains('navbar-solid')).toBe(true);
    expect(navbar.classList.contains('navbar-transparent')).toBe(false);

    // Scroll back above trigger
    window.scrollY = 10;
    window.dispatchEvent(new Event('scroll'));

    expect(navbar.classList.contains('navbar-solid')).toBe(false);
    expect(navbar.classList.contains('navbar-transparent')).toBe(true);
  });

  test('navbar recalculates trigger on resize and orientationchange', () => {
    loadScript();
    const navbar = document.getElementById('navbar');

    // Make trigger smaller via resize (innerHeight => 200 -> trigger = 30)
    window.innerHeight = 200;
    window.dispatchEvent(new Event('resize'));

    // Now crossing 30 should toggle solid
    window.scrollY = 50;
    window.dispatchEvent(new Event('scroll'));
    expect(navbar.classList.contains('navbar-solid')).toBe(true);

    // Change again via orientationchange; trigger recalculated
    window.innerHeight = 400; // trigger = 60
    window.dispatchEvent(new Event('orientationchange'));

    // With scrollY=50 (<60) it should go back to transparent after update()
    window.dispatchEvent(new Event('scroll'));
    expect(navbar.classList.contains('navbar-solid')).toBe(false);
  });

  test('visibilitychange forces an update when tab becomes visible', () => {
    loadScript();
    const navbar = document.getElementById('navbar');

    // Ensure below threshold initially
    window.scrollY = 0;
    expect(navbar.classList.contains('navbar-solid')).toBe(false);

    // Change scroll behind the scenes, then simulate returning to page
    window.scrollY = 500;
    Object.defineProperty(document, 'visibilityState', { value: 'visible', configurable: true });
    document.dispatchEvent(new Event('visibilitychange'));

    expect(navbar.classList.contains('navbar-solid')).toBe(true);
  });

  test('highlightCurrentNavLink marks the current page link active and ignores external/hash/mailto', () => {
    loadScript();

    const links = Array.from(document.querySelectorAll('.nav-link'));
    const root = links.find(a => a.getAttribute('href') === '/');
    const about = links.find(a => a.getAttribute('href') === '/about');
    const external = links.find(a => a.getAttribute('href')?.startsWith('https'));
    const hash = links.find(a => a.getAttribute('href')?.startsWith('#'));
    const mail = links.find(a => a.getAttribute('href')?.startsWith('mailto:'));

    // current path is /about/ (with trailing slash), script normalises both sides
    expect(about.classList.contains('active')).toBe(true);

    expect(root.classList.contains('active')).toBe(false);
    expect(external.classList.contains('active')).toBe(false);
    expect(hash.classList.contains('active')).toBe(false);
    expect(mail.classList.contains('active')).toBe(false);
  });

  test('defensive: no crash if #navbar absent or no .nav-link elements', () => {
    document.body.innerHTML = `<div>no navbar or links here</div>`;
    loadScript(); // should not throw
  });
});
