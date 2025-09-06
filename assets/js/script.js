// scripts/include.js loads in global navbar and footer

async function loadIncludes() {
  const header = await fetch("header.html").then(res => res.text());
  const footer = await fetch("footer.html").then(res => res.text());

  document.getElementById("header").innerHTML = header;
  document.getElementById("footer").innerHTML = footer;

  // Call scroll initializer after navbar is loaded into the DOM
  initNavbarScrollEffect();

  // Highlight the current nav link
  setTimeout(() => {
    const current = window.location.pathname.split("/").pop() || "index.html";
    document.querySelectorAll(".nav-link").forEach(link => {
      if (link.getAttribute("href") === current) {
        link.classList.add("active");
      }
    });
  }, 100);
}

loadIncludes();

// Function to initialize scroll event listener for navbar
function initNavbarScrollEffect() {
  const navbar = document.getElementById("navbar");
  if (!navbar) return;

  window.addEventListener("scroll", () => {
    const scrollTrigger = window.innerHeight * 0.3; // 30% of viewport height

    if (window.scrollY > scrollTrigger) {
      navbar.classList.add("navbar-solid");
      navbar.classList.remove("navbar-transparent");
    } else {
      navbar.classList.add("navbar-transparent");
      navbar.classList.remove("navbar-solid");
    }
  });
}
