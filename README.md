# UK Winter Mountain Tours V2

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/TGOSS1984/uk_winter_mountain_tours_v2/actions)
![Coverage](docs/badges/coverage.svg)
[![Deployment](https://img.shields.io/badge/heroku-live-purple)](https://uk-winter-mountain-tours-v2-c6f21d80d2c8.herokuapp.com/)
![CI – Tests](https://github.com/TGOSS1984/uk_winter_mountain_tours_v2/actions/workflows/test.yml/badge.svg)

## Introduction

A full-stack Django web application providing guided winter mountain tours across the UK.  
Features include interactive GPX route maps, online bookings (with double-booking prevention), cancellations, and region-specific route pages.

This project is also a personal passion of mine, reflecting my long-standing interest in the outdoors and mountain environments. My very first coding project was a simple guided tours website built with only HTML and CSS. This application can be seen as its “spiritual successor” — rebuilt from the ground up with Django, Python, Bootstrap, Leaflet, and Heroku — and hopefully demonstrates the progress I have made in both technical skills and project depth since then.

Building this application has been a journey of learning and discovery. Django in particular came with a steep but rewarding learning curve. Implementing authentication, user profiles, and email notifications required not only understanding the framework’s built-in tools but also extending them thoughtfully, and I feel this marks a big step forward in my ability to work with a complex backend framework. Along the way, I encountered and resolved a number of issues — from template syntax errors to failing GitHub Actions builds — and each challenge became an opportunity to strengthen my debugging and problem-solving skills.

The project’s scope grew steadily as I worked through both required features and “nice to haves.” I learned to prioritise features that mapped directly to assessment learning outcomes, such as notifications for LO2.3 and authentication for LO3, while keeping an eye on broader polish and usability. One of the most important lessons I took away was the value of a clean, consistent folder and file structure. As the application grew in size, maintaining a clear separation of apps, templates, static files, fixtures, and services became critical, both for readability and for smooth deployment to Heroku.

Testing and continuous integration also played a much greater role in this project than in my earlier work. Writing targeted unit tests for bookings and email notifications, and integrating GitHub Actions to automatically run them, gave me hands-on experience of defensive design and the reassurance of automated checks whenever I pushed new code. This felt like a major step towards “real-world” development practices.

Although the project already delivers a complete and working product, there remains room for future improvements. I can see scope for features such as asynchronous email delivery, richer profile information, or enhanced admin dashboards. The current build represents a solid foundation, but it also leaves space for iteration, refinement, and further learning.

In short, this project has been both a technical and personal milestone, combining my passion for the outdoors with practical full-stack development skills, and showing me how much can be achieved when good design, careful structure, and persistence come together.



![Image from mockup](assets/images/screenshots/ux/homepage_mockup.PNG)


---

## 📑 Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [User Stories](#user-stories)
- [System Architecture](#system-architecture)
- [Data Model](#data-model)
- [Project Structure](#project-structure)
- [Rationale & Design Decisions](#rationale--design-decisions)
- [Wireframes & Mockups](#wireframes--mockups)
- [Accessibility & UX](#accessibility--ux)
- [Performance](#performance)
- [Technologies Used](#technologies-used)
- [Installation & Local Setup](#installation--local-setup)
- [Environment Variables](#environment-variables)
- [Database & Fixtures](#database--fixtures)
- [Testing](#testing)
- [Linting](#linting)
- [CI/CD & Deployment](#cicd--deployment)
- [Assessment Criteria Mapping (LO1–LO9)](#assessment-criteria-mapping-lo1lo9)
- [Screenshots](#screenshots)
- [Lighthouse Results](#lighthouse-results)
- [🔧 Major Bugs & Fixes](#-major-bugs--fixes)
- [Future Improvements](#future-improvements)
- [Credits](#credits)

---

## Project Overview

This project simulates a real-world guided tours booking system, built with Django.  
It integrates mapping (Leaflet + GPX overlays), booking management with cancellation, validation, email notifications, and dynamic region pages.

**Key goals**
- Deliver an end-to-end booking platform.
- Integrate real-world route data (GPX) with interactive maps.
- Ensure accessibility, responsiveness, and performance.
- Deploy to Heroku with production-ready settings.

---

## Features


- Region pages: Lake District, Wales, Scotland, Peak District/Yorkshire Dales.  
- GPX route overlays with Leaflet maps.  
- Booking system with **double-booking prevention**.  
- Cancel bookings via booking detail page.  
- Admin interface for guides, routes, and bookings.  
- Responsive UI with Bootstrap 5.  
- Javascript on-scroll navbar.  
- Accessibility enhancements (contrast, alt text, keyboard-friendly).  
- Static/media assets served via **Whitenoise** in production.  
- **Email Notifications**:  
  When a user books or cancels a tour, the system generates a confirmation or cancellation email.  
  - In **development**, these are sent to the console backend so developers and assessors can see the message output.  
  - In **CI tests**, a locmem backend captures emails to verify delivery.  
  - In **production**, the feature is configurable — an SMTP backend (e.g. SendGrid) can be enabled by toggling environment variables, though by default email sending is disabled for stability.  
- **Authentication & Profiles**:  
  - Email is required when creating an account, ensuring every user can receive notifications.  
  - Login accepts either **username or email** for convenience.  
  - Profiles are auto-created for each user, extendable with extra fields (e.g. phone). 


---

## User Stories

Examples:

1. **As a user, I want to browse tours in different regions, so I can decide where to hike.**  
   - **Implementation:** Region pages at `templates/pages/regions/` (`lake_district.html`, `peak_district.html`, `scotland.html`, `wales.html`); data seeded from `bookings/fixtures/routes.json`  
   - **URLs:** `/regions/lake-district/`, `/regions/peak-district/`, `/regions/scotland/`, `/regions/wales/`  
   - **Tests:** `bookings/tests/test_views.py` (region pages render routes)

2. **As a user, I want to view routes on a map with elevation paths, so I can plan my day.**  
   - **Implementation:** Leaflet init inside the region templates in `templates/pages/regions/*.html`; GPX files under `static/gpx/`  
   - **Tests:** `bookings/tests/test_views.py` (map container present); **Manual:** verify GPX overlay renders

3. **As a user, I want to book a tour and receive confirmation, so I can secure my spot.**  
   - **Implementation:** `bookings/views.py` (create view), `bookings/models.py` (`Booking`), form template `templates/bookings/booking_form.html`  
   - **Tests:** `bookings/tests/test_forms.py` (valid form), `bookings/tests/test_views.py` (create view happy path); **Manual:** success flash/message

4. **As a user, I want to cancel a booking if my plans change.**  
   - **Implementation:** `bookings/views.py` (cancel view/endpoint), cancel UI in `templates/bookings/booking_list.html`  
   - **Tests:** `bookings/tests/test_views.py` (cancel flow)

5. **As an admin, I want to add/edit guides and routes, so I can keep offerings up to date.**  
   - **Implementation:** Django Admin `bookings/admin.py`  
   - **Tests:** **Manual:** CRUD in Admin (create/edit/delete)

6. **As an admin, I want to seed routes/guides from fixtures, so the database can be reset easily.**  
   - **Implementation:** Fixtures `bookings/fixtures/dev_seed.json`, `bookings/fixtures/routes.json`  
   - **Tests:** **Manual:** `python manage.py loaddata dev_seed.json routes.json`; `dumpdata` documented

7. **As a visitor, I want the site to be accessible on mobile, so I can use it while travelling.**  
   - **Implementation:** Responsive Bootstrap templates in `templates/pages/*.html` and `templates/includes/*`; Leaflet mobile support  
   - **Tests:** **Manual:** device/browser checks; Lighthouse Mobile screenshots in `docs/screenshots/`

8. **As a user, I want the site to be performant and accessible, so I can navigate without issues.**  
   - **Implementation:** Contrast/focus styles (Leaflet control CSS), semantic headings, ARIA labels in templates  
   - **Tests:** **Manual:** Lighthouse ≥ 90 Accessibility; Axe audit results

9. **As a user, I want to receive an email when I book or cancel a tour, so I have a clear record.**
  - **Implementation:** Email service in bookings/services.py (transaction-safe via on_commit); templates in templates/email/booking_confirmation.{txt,html} and booking_cancellation.{txt,html}; wired in bookings/views.py (BookingCreateView.form_valid() and cancel_booking). Feature-flagged by ENABLE_EMAIL_NOTIFICATIONS with DEFAULT_FROM_EMAIL + EMAIL_BACKEND in settings/env.
  - **Tests:** bookings/tests/test_emails.py (uses TransactionTestCase + locmem backend).
  - **Manual:** In dev, console backend prints the email to the terminal; in prod, enable SMTP via env (documented in README).
10. **As a user, I want to log in with my email or username, so I don’t have to remember a separate credential.**
  - **Implementation:** core/forms.py LoginForm accepts email or username, updates field label to “Username or Email”; routed via custom LoginView in urls.py (custom login path before django.contrib.auth.urls).
  - **Tests:Manual:**verify both email+password and username+password paths work on /accounts/login/.
11. **As a user, I want email to be required at signup, so I can receive notifications and recover my account.**
  -**Implementation:**core/forms.py SignupForm (extends UserCreationForm), adds required, unique email; SignupView uses SignupForm; templates/registration/signup.html uses {{ form.as_p }} so the email field renders automatically.
  - **Tests:Manual:**signup rejects duplicate/blank emails; visible field + validation errors on the form.

**Acceptance Criteria Template**
- Given I am on the **Region** page, when I click a route card, then I should see the route detail with a Leaflet map and a visible GPX overlay.
- Given I select a **guide/date/time**, when I submit a valid booking, then the booking is created and I see a success message.
- Given a **conflicting timeslot**, when I attempt to book the same guide, then I receive a validation error preventing double booking.
- Given I have a booking, when I click "Cancel booking", then the booking is deleted and I see a success message.
- Given I try to cancel a booking that doesn’t exist, when I click the button, then I see a friendly error and no crash.


| Story                | Feature(s)                                                                 | Tests / Evidence                                |
|-----------------------|-----------------------------------------------------------------------------|------------------------------------------------|
| Browse tours          | `templates/pages/regions/*.html`, `bookings/fixtures/routes.json`          | `bookings/tests/test_views.py`                 |
| View map              | Leaflet init in `templates/pages/regions/*.html`, `static/gpx/*.gpx`       | `bookings/tests/test_views.py`; Manual GPX render |
| Book a tour           | `bookings/views.py`, `bookings/models.py`, `templates/bookings/booking_form.html` | `bookings/tests/test_forms.py`, `bookings/tests/test_views.py` |
| Cancel booking        | `bookings/views.py` (cancel), `templates/bookings/booking_list.html`       | `bookings/tests/test_views.py`                 |
| Prevent double booking| `bookings/models.py` (UniqueConstraint / validation)                       | `bookings/tests/test_models.py` (or `test_views.py`) |
| Admin manage          | `bookings/admin.py`                                                        | Manual CRUD in Admin                           |
| Accessibility         | Template semantics + CSS focus/contrast                                    | Lighthouse & Axe screenshots                   |


---

## System Architecture

- **Backend:** Django project with modular apps (`bookings`, `core`, `mountain_tours_v2`).
- **Frontend:** Django templates with Bootstrap; Leaflet + GPX plugin for maps.
- **Static files:** Served locally via `django.contrib.staticfiles`; in production via **Whitenoise**.
- **Database:** SQLite in development; Heroku Postgres in production (recommended).
- **Deployment:** Heroku using `Procfile` and environment variables.

**High-Level Flow**
```
Client (Browser) → Django URLs → Views → Templates
                               ↘ Models (DB)
Static/Media (via Whitenoise)  ↘ Leaflet JS (GPX overlays)
```

![System Architecture](docs/screenshots/architecture.png)

---

## Data Model

**Core Entities**
- `Guide(id, name, email, phone, bio)`
- `Route(id, name, region, gpx_path, description, distance_km, elevation_gain_m, ... )`
- `Booking(id, guide, route, date, time_start, time_end, customer_name, customer_email, status)`

**Business Rules**
- Prevent double-booking of the same guide/time slot.
- Optional: enforce route capacity per day.

*(STILL TO COMPLETE: ERD diagram in /docs/screenshots/erd.png and brief explanation of relationships.)*

---

## Project Structure

```
UK_WINTER_MOUNTAIN_TOURS_V2/
│
├── .github/                # GitHub Actions workflows (CI) (STILL TO COMPLETE)
├── assets/                 # Static assets (images, icons, favicons, js, css)
├── bookings/               # Bookings app (models, views, fixtures, services,tests)
├── core/                   # Core settings / config
├── docs/                   # System architecture
├── mountain_tours_v2/      # Project entry app
├── node_modules/           # Node.js dependencies
├── templates/              # Django templates (HTML pages)
├── tests/                  # Python tests
├── tools/                  # Utility scripts (used to resize / rename images)
│
├── .env.example            # Example environment file
├── .gitignore
├── .slugignore
├── babel.config.js
├── db.sqlite3              # Dev DB
├── jest.config.js          # Jest config
├── manage.py
├── package.json            # Node config
├── package-lock.json
├── Procfile                # Heroku config
├── README.md               # Project documentation
├── requirements.txt        # Python runtime dependencies
```

*(STILL TO COMPLETE: add Ruff/ESLint configs, requirements-dev.txt, pyproject.toml once added.)*

---

## Rationale & Design Decisions

## Rationale & Design Decisions

- **Why Django?** Rapid development, batteries-included admin, robust ORM, clear separation of concerns.  
- **Leaflet + GPX:** Lightweight, flexible mapping with client-side overlays for GPX files.  
- **Whitenoise for static files:** Simple, zero-extra-infra static serving on Heroku.  
- **Fixtures-first approach:** Keep dev/prod data consistent via `dumpdata/loaddata` workflows.  

- **Require email at signup:** Email is mandatory on account creation so every user can be contacted. This is practical (no “orphan” accounts without contact info) and directly addresses **LO2.3 (notify relevant user)**.  
- **Service-based email sending:** Implemented notifications in `bookings/services.py` instead of views. This keeps responsibilities clear, makes testing easier, and avoids logic duplication.  
- **Login by username *or* email:** Improves usability by letting users sign in with whichever credential they remember. This leverages Django’s auth system without introducing a custom user model, striking a balance between UX and complexity.  


*(STILL TO COMPLETE: note trade-offs—client-side GPX parsing vs server-side preprocessing; SQLite vs Postgres locally.)*

---

## Wireframes & Mockups

- Home page wireframe  
  ![Homepage Mockup](assets/images/screenshots/wireframes/wireframe_homepage_mockup.PNG)
- Region/Route wireframe  
  ![Region/Route Mockup](assets/images/screenshots/wireframes/wireframe_regions_mockup.PNG)

---

## Accessibility & UX

- Bootstrap grid for responsive design.
- Improved contrast on Leaflet map controls and attribution.
- Keyboard-friendly navigation; offcanvas mobile menu.

**Checklist**
- [ ] All interactive elements are reachable via keyboard.
- [ ] `aria-label` / `aria-expanded` set on nav toggles.
- [ ] Images include descriptive `alt` text or are decorative.
- [ ] Sufficient color contrast on text and controls.

### Accessibility & UX Manual Checks

- **Keyboard navigation:**  
  Verified that all nav links, buttons, and form fields are reachable via `Tab`. Leaflet map controls can be reached, but focus styling could be improved (marked as Partial in manual tests).  
- **Screen reader spot-checks:**  
  Used NVDA/VoiceOver to confirm that headings, nav landmarks, and form labels are announced correctly. ARIA labels were added where necessary. Maps announce as “interactive” but route traces are not fully described — future enhancement.  
- **Login:**
  User can login using email OR username at sign in. Plus confirmation emails can improve clarity & trust


---

## Performance

- Image sizing (`object-fit`, responsive images); potential use of `loading="lazy"` on non-critical images.
- Static file compression via Whitenoise.
- Minimal external scripts; async/defer where possible.

*(STILL TO COMPLETE: Add Lighthouse scores + actions taken to improve.)*

---

## Technologies Used

- **Backend:** Django (Python 3.11), Django email backends (console + locmem for tests), Django built in auth system
- **Frontend:** Bootstrap 5, Leaflet.js (+ Leaflet GPX plugin)
- **Database:** SQLite (dev), Postgres (Heroku recommended)
- **Testing:** Django test framework, Jest (frontend)
- **DevOps:** Heroku, GitHub Actions (planned/partial)
- **Linting:** Ruff, ESLint/Prettier

---

## Installation & Local Setup

1. **Clone repo**
   ```bash
   git clone <repo-url>
   cd UK_WINTER_MOUNTAIN_TOURS_V2
   ```

2. **Create virtualenv & install Python requirements**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   # source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Install Node dependencies**
   ```bash
   npm install
   ```

4. **Set up environment**
   - Copy `.env.example` → `.env`
   - Adjust values for local dev

5. **Migrate & seed database**
   ```bash
   python manage.py migrate
   python manage.py loaddata bookings/fixtures/dev_seed.json
   # Optional: also load routes.json if split
   # python manage.py loaddata bookings/fixtures/routes.json
   ```

6. **Run server**
   ```bash
   python manage.py runserver
   ```

7. **Emails**


---

## Environment Variables

From `.env.example`:
```
DEBUG=1
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=
SECRET_KEY=change-me
```
*(STILL TO COMPLETE: add `DATABASE_URL` for Heroku Postgres; secure cookie and security headers for production.)*

Recommended production additions:
```
DEBUG=0
ALLOWED_HOSTS=your-domain.com, your-heroku-app.herokuapp.com
CSRF_TRUSTED_ORIGINS=https://your-heroku-app.herokuapp.com,https://your-domain.com
DATABASE_URL=postgres://...
```

---

## Database & Fixtures

- **Fixtures live in** `bookings/fixtures/dev_seed.json` and `routes.json`.
- **Workflow:**
  - Update data via Django Admin.
  - Export to fixtures:
    ```bash
    python manage.py dumpdata bookings > bookings/fixtures/dev_seed.json
    ```
  - Import fixtures:
    ```bash
    python manage.py loaddata bookings/fixtures/dev_seed.json
    ```
- Ensure JSON encoding is **UTF-8**.

*(STILL TO COMPLETE: add sample commands for splitting guides/routes fixtures if needed.)*

---

## Testing

### Django Tests
Run backend tests:
```bash
python manage.py test
```

### Running tests
- Local: `python -m pytest -v -ra`

### Coverage
This project uses **pytest-cov** to measure test coverage.
- Install: `pip install pytest-cov`
- Run: `python -m pytest --cov=bookings --cov-report=term-missing --cov-report=html`
  - HTML report: `htmlcov/index.html`
- In CI: Coverage is generated on every push to `main`, and the badge below is auto-updated.

![Coverage](docs/badges/coverage.svg)

### Jest Tests
Run frontend tests:
```bash
npm test
```

### Suggested Coverage Targets
- Booking model/form validation (double-booking).
- Views: booking create/cancel flows (happy & edge paths).
- JS: Leaflet map initialisation; graceful handling when GPX not found.

### Test Evidence
- Django tests passing  
  ![Terminal Test Screenshot Placeholder](assets/images/screenshots/tests/terminal_pytest_test.PNG)
  ![Github actions Django Test Screenshot Placeholder](assets/images/screenshots/tests/django_tests.PNG)
- Jest tests passing  
  ![Terminal Test Screenshot Placeholder](assets/images/screenshots/tests/terminal_jest_test.PNG)
  ![Github actions Jest Test Screenshot Placeholder](assets/images/screenshots/tests/jest_tests.PNG)

### Manual Testing
In addition to automated tests, targeted **manual testing** validated real user flows and edge cases (mobile nav, 404/CSRF handling, GPX fallbacks, admin CRUD, fixture round-trips, accessibility of map controls).

### Manual Test Matrix (samples)

| Area | Steps | Expected | Result |
|---|---|---|---|
| Past-date booking blocked | Go to booking form → choose yesterday → submit | Form refuses; clear validation message shown; no record created | ✅ Pass |
| Cancel past booking | Create a booking in the past (or mock) → try cancel | Cancellation disallowed; friendly message; no state change | ✅ Pass |
| Missing GPX fallback | Point a route to `static/gpx/missing.gpx` → load page | Map loads without crash; shows fallback/help text; no console errors | ⚠️ Partial – currently throws console error; future enhancement to add fallback |
| 404 on bad region | Visit `/regions/not-a-real-region/` | Custom 404 page; no stacktrace | ✅ Pass (custom/standard 404 shown in production) |
| Keyboard nav | Tab through region page & map controls | Visible focus, logical order; controls usable via keyboard | ⚠️ Partial – Bootstrap handles links/buttons, but focus styles still need review |
| OS Maps attribution | Load any route with map | Attribution visible and focusable; meets compliance | ✅ Pass |
| Off-canvas nav mobile | Open menu → tap “About” | Navigates, menu closes, scroll enabled, focus returns to toggler | ✅ Pass |
| CSRF protection | Remove token via DevTools → submit booking | 403 CSRF; no server error | ✅ Pass |
| Admin CRUD | Add/edit/delete a Route in Admin | Public pages reflect changes; no broken links | ✅ Pass |
| Fixtures round-trip | `dumpdata` → reset DB → `loaddata` | Routes/guides restored; pages render; no FK errors | ✅ Pass |


---

## Linting

- **Python:** [Ruff](https://github.com/astral-sh/ruff) for linting and import order.  
  - Local: `ruff check .` (autofix imports: `ruff check . --select I --fix`)
- **JavaScript:** ESLint + Prettier for code style.  
  - Local: `npm run format:check` and `npm run lint:js`

In CI, lint checks run in a non-blocking mode initially. Once the codebase is clean, they can be enforced by removing the non-blocking guards.

---

## CI/CD & Deployment

- **GitHub Actions**: run Django & Jest tests on push/PR *(STILL TO COMPLETE: add Node/Python linters and coverage upload)*.
- **Heroku**: deploy with `Procfile`; run `collectstatic` during release.
- **Static files**: served by Whitenoise (ensure `MIDDLEWARE` includes it).
- **Emails** : verified in CI using locmen backend. Console backend used in dev, SMTP in production


*(STILL TO COMPLETE: add pipeline diagram /docs/screenshots/cicd-pipeline.png and auto-deploy notes.)*

---

## Assessment Criteria Mapping (LO1–LO9)

**LO1 — Planning & Design**
- Problem statement & scope ✅
- Architecture & data model rationale ✅
- Wireframes/user flows ✅

**LO2 — Data, Algorithms & Validation**
- Core models & relationships ✅
- Business rules (no double booking) ✅
- Defensive validation documented ⚠️ *(Add negative-path tests)*

**LO3 — Implementation & Code Quality**
- Django app structure with maps ✅
- Frontend responsiveness ✅
- Linters (Ruff/ESLint) ✅

**LO4 — Testing**
- Django tests ✅
- Jest tests ✅
- Coverage reporting ✅
- Optional E2E (Playwright) ⬜

**LO5 — Robustness, Error Handling & Security**
- Error messages for forms ✅
- Production settings docs ⚠️ *(Add `DEBUG=False`, headers, CSP)*
- Custom 4xx/5xx pages ⬜

**LO6 — Version Control & Workflow**
- Granular commits & messages ✅
- Branching/PRs summary ⚠️ *(Document briefly in README)*

**LO7 — Deployment & DevOps**
- Heroku deploy ✅
- CI tests on push/PR ✅
- Postgres in prod ⬜ *(Confirm & document)*

**LO8 — Documentation & Professional README**
- Feature overview, setup, testing ✅
- Fixtures workflow ✅
- Screenshots, diagrams ✅

**LO9 — UX, Accessibility & Performance**
- Responsive layout ✅
- Accessibility improvements ✅
- Lighthouse scores ⬜

Legend: ✅ covered | ⚠️ partial | ⬜ outstanding


---

## Screenshots

- Home page  
  ![Home Page](assets/images/screenshots/ux/homepage.PNG)
- Region page with GPX map  
  ![Region Page](assets/images/screenshots/ux/region_gpx.PNG)
- Booking form  
  ![Booking Form](assets/images/screenshots/ux/booking.PNG)
- Booking confirmation  
  ![Booking Cancellation](assets/images/screenshots/ux/booking_create.PNG)

---

## Lighthouse Results

- Performance  
  ![Placeholder](docs/screenshots/lighthouse-performance.png)
- Accessibility  
  ![Placeholder](docs/screenshots/lighthouse-accessibility.png)
- Best Practices  
  ![Placeholder](docs/screenshots/lighthouse-bestpractices.png)
- SEO  
  ![Placeholder](docs/screenshots/lighthouse-seo.png)

*(STILL TO COMPLETE: include Lighthouse run command and key fixes implemented.)*

---

## 🔧 Major Bugs & Fixes

**GPX files not displaying on Leaflet maps**  
- **Bug:** GPX overlays failed to load on region pages (e.g., Lake District, Wales), either due to incorrect file paths or missing references.  
- **Fix:** Ensured GPX files were stored under `static/routes/` (or referenced in templates correctly). Used `{% static %}` in `<script>`/Leaflet GPX calls to make Django serve them.

**Hero images / background PNGs not appearing**  
- **Bug:** Hero/overlay PNG backgrounds didn’t render, even though paths looked correct.  
- **Fix:** Adjusted CSS to use `background: url("{% static 'images/...png' %}")` inside templates, and confirmed files were in `static/images/hero/`. Also resolved issues with `background` vs `background-color` shorthand overriding.

**Deployment to Heroku not serving static files**  
- **Bug:** After deployment, static assets (images, CSS, JS, GPX) didn’t load.  
- **Fix:** Installed and configured **Whitenoise** in `settings.py`, collected static files (`python manage.py collectstatic`), and checked case-sensitive paths (`.PNG` vs `.png`).

**Heroku not showing newly added routes from JSON**  
- **Bug:** Extra routes added to `routes.json` locally didn’t appear in deployed version.  
- **Fix:** Updated fixture files (`bookings/fixtures/dev_seed.json` and `routes.json`), re-ran `loaddata` locally, pushed to GitHub, and re-deployed to Heroku. Ensured JSON saved with **UTF-8** encoding.

**Seeding issues with fixtures**  
- **Bug:** Unsure how to keep dev and production JSON in sync (guides, routes). Some data missing when deploying.  
- **Fix:** Used `python manage.py dumpdata bookings > bookings/fixtures/dev_seed.json` to export from local DB, then re-import with `loaddata` to seed both `dev_seed.json` and `routes.json`.

**Double bookings allowed initially**  
- **Bug:** System didn’t prevent users from booking the same guide/date/time more than once.  
- **Fix:** Added logic in the booking model/form to check availability before saving. Now prevents duplicates.

**Navbar and routing issues after deployment**  
- **Bug:** Links (like “About” or “Booking”) sometimes didn’t resolve properly on mobile nav/offcanvas.  
- **Fix:** Updated `href="{% url '...' %}"` to use Django URL names consistently and fixed offcanvas toggler attributes.

---

## Future Improvements

- Add Postgres locally to match Heroku (via Docker or `psycopg`).
- Expand Jest test coverage (UI, map loading); add mocks for Leaflet/GPX.
- Add Ruff + ESLint/Prettier lint checks in CI.
- Add Playwright end-to-end “browse → select route → book → cancel” flow.
- Add Content Security Policy (CSP) with Leaflet tile/CDN allowances.
- Add screenshots, architecture diagram, ERD, and coverage badges.
- Asynchronous email (Celery).
- Richer profiles (phone, preferences).
- Admin email on booking.

---

## Credits

- **Leaflet.js** – for interactive mapping.  
- **Leaflet GPX plugin** – for route overlays.  
- **Bootstrap 5** – for responsive frontend layout.  
- **Heroku** – for deployment.  
- **Ordnance Survey / GPX providers** – for route data.  
- **Django & Python open-source community** – for frameworks and libraries.  
- **AI assistance (ChatGPT)** – used as a support tool for documentation tasks such as README formatting, template examples, to-do checklists, and structuring notes.  
  All coding, testing, and implementation decisions were completed by me.  
  - **Images** – Logo created by Tom Goss, gallery images actual photos from winter hikes, other images google images 

---
