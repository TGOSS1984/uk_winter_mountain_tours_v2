# Mountain Tours v2 — Full‑Stack Django Project (Beginner‑Friendly, UX‑Preserving)

A full‑stack website for booking guided mountain tours across UK regions. This starter keeps your **existing HTML/CSS/JS** intact and adds a clean Django backend (auth, bookings, data model, tests, deployment files). It is designed to meet the **Portfolio Project 4 – Full‑Stack Toolkit** criteria (Pass → Merit → Distinction).


---

## 1) Quickstart

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000

---

## 2) Project Purpose

- Let users **browse regions** (Lake District, Scotland, Wales, Peak District).  
- Allow authenticated users to **book a guide** for a route at a date/time slot (AM/PM).  
- **Prevent double bookings** per guide per date/time with a DB unique constraint + validation.  
- Deliver a **clean, responsive, accessible** UI.  
- Deploy on a cloud host with **Postgres** using environment variables.

---

## 3) Tech Stack

- **Django 5** (templates, models, auth, admin)  
- **Postgres** (via `DATABASE_URL`), **SQLite** by default for development  
- **WhiteNoise** for static files in production  
- **Gunicorn** (`Procfile`)  
- **python‑dotenv** & **dj‑database‑url** for env‑driven config

---

## 4) Folder Structure

```
mountain_tours_v2/
├─ manage.py
├─ requirements.txt
├─ Procfile
├─ .gitignore
├─ .env.example
├─ mountain_tours_v2/            # settings/urls/wsgi/asgi
│  ├─ settings.py
│  ├─ urls.py
│  ├─ asgi.py
│  └─ wsgi.py
├─ core/                         # public pages + signup
│  ├─ urls.py
│  ├─ views.py
│  ├─ tests.py
│  └─ admin.py
├─ bookings/                     # Guide/Route/Booking models + views/forms
│  ├─ models.py
│  ├─ forms.py
│  ├─ views.py
│  ├─ urls.py
│  ├─ tests.py
│  └─ migrations/__init__.py
├─ templates/
│  ├─ base.html
│  ├─ includes/
│  │  ├─ header.html             # uses your header if provided
│  │  └─ footer.html             # uses your footer if provided
│  ├─ pages/
│  │  ├─ index.html              # placeholder (replace with your index when ready)
│  │  ├─ equipment.html          # placeholder
│  │  ├─ gallery.html            # placeholder
│  │  └─ regions/
│  │     ├─ lake_district.html   # **your** Lake District page integrated
│  │     ├─ scotland.html        # stub (paste your HTML later)
│  │     ├─ wales.html           # stub
│  │     └─ peak_district.html   # stub
│  ├─ bookings/
│  │  ├─ booking_form.html
│  │  └─ booking_list.html
│  └─ registration/
│     ├─ login.html
│     └─ signup.html
├─ assets/
│  ├─ css/   # your CSS copied here (unchanged filenames)
│  ├─ js/    # your JS copied here (unchanged filenames)
│  ├─ favicon/
│  └─ images/  # empty; add your images later
└─ routes/
   ├─ lake_district/   # your GPX files copied here
   ├─ scotland/
   ├─ wales/
   └─ peak_district/
```

---

## 5) Data Model (OOP)

- **Guide**: `name`, `email`, `phone`, `bio`
- **Route**: `name`, `region` (`lake_district|scotland|wales|peak_district`), `gpx_path`, `distance_km`, `duration_hours`
- **Booking**: `user`, `customer_name`, `customer_email`, `route`, `guide`, `date`, `time_slot` (`AM|PM`), `status` (`confirmed|cancelled`), `created_at`
  - `UniqueConstraint(guide, date, time_slot)` **prevents double bookings**.
  - `clean()` validation enforces business rules.

**Relationships:** User 1—*N* Booking; Guide 1—*N* Booking; Route 1—*N* Booking.

---

## 6) Features (MVP)

- Public pages (index, equipment, gallery, regions).  
- Auth (login/logout + signup).  
- Book a tour (`/bookings/new/`) — logged‑in only.  
- List my bookings (`/bookings/`).  
- Django Admin for Guides/Routes/Bookings.

**Next (optional) for full CRUD:** Edit/cancel bookings + staff/guide roles.

---

## 7) URLs

- `/` — home  
- `/equipment/`, `/gallery/` — info pages  
- `/regions/lake-district/` — **your** Lake District page (Django template)  
- `/regions/scotland/`, `/regions/wales/`, `/regions/peak-district/` — stubs  
- `/bookings/` — my bookings (auth required)  
- `/bookings/new/` — create booking (auth required)  
- `/accounts/login`, `/accounts/logout`, `/signup` — auth

---

## 8) Keeping Your UX Exactly the Same

- Your **CSS/JS** copied into `assets/` as‑is.  
- Your Lake District HTML is wrapped with `{% extends 'base.html' %}` and inserted into `{% block content %}`; any page‑specific `<link>`/`<script>` from your `<head>` are injected into `{% block extra_head %}` / `{% block extra_scripts %}` so nothing breaks.  
- To port more pages, paste your HTML into the corresponding template file and keep your classes/IDs unchanged.

---

## 9) Testing

### Python (Django)
- **Unit tests** (in `bookings/tests.py`):
  - Double booking is rejected by validation.
  - Booking list view requires login.
- Add more tests as you implement features (e.g., form validation, permissions).

### JavaScript
- If you add complex client logic, you can add a small Jest setup for unit tests and document it here.

---

## 10) Deployment (Render/Railway/Other PaaS)

1. Create a Postgres DB and obtain `DATABASE_URL`.
2. Set environment variables:
   - `SECRET_KEY` (random string)
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-app.onrender.com,yourdomain.com`
   - `DATABASE_URL=postgres://...`
3. Build steps:
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
4. Start command: `gunicorn mountain_tours_v2.wsgi`
5. Confirm the deployed site matches local; remove commented code and fix any broken links.

**Security:** No secrets in Git; DEBUG off in production; CSRF enabled; permissions respected.

---

## 11) Mapping to Assessment Criteria

### Pass — Learning Outcomes

**LO1 – Agile planning & MVC design**
- Front‑end designed to accessibility & UX guidelines (semantic HTML, responsive layout).  
- Django MVC structure: `core`/`bookings` apps, templates, static assets.  
- Use a GitHub Project board for **Epics → Stories → Tasks**; write acceptance criteria.

**LO2 – Data model & business logic**
- Models for Guide/Route/Booking; unique constraint prevents double bookings.  
- CRUD path (Create + Read now; update/cancel next).  
- Validated forms (`BookingForm`) with server‑side validation.

**LO3 – Auth & permissions**
- Login/logout + signup; restricted booking views (login required).  
- (Next) Add staff/guide roles with Django Groups/Permissions.

**LO4 – Testing**
- Python tests provided; extend coverage.  
- (Optional) JS tests if adding dynamic features.

**LO5 – Git & GitHub**
- Use Git for version control; commit frequently with descriptive messages.  
- No secrets committed; `.gitignore` included.

**LO6 – Deployment**
- Procfile, requirements.txt, static pipeline with WhiteNoise.  
- Document deployment steps, env vars, and turning `DEBUG` off.

**LO7 – Object‑based concepts**
- Custom model classes and relationships; forms/views follow Django patterns.

### Merit — Additional Evidence
- Clear rationale & target audience in README.  
- Full CRUD including **update** and **cancel** bookings.  
- Robust input validation & user feedback (messages).  
- Purpose obvious to new users; responsive design; no logic errors.  
- Data schema diagram included & explained.  
- Centralised DB config via `DATABASE_URL`.  
- Frequent, small commits with clear messages.  
- Detailed, well‑structured deployment docs.

### Distinction — Craftsmanship & Professional Finish
- Polished, accessible UI with consistent interaction patterns and feedback.  
- Defensive design: validation + graceful error handling; no broken links; back/forward nav safe.  
- Clean code: naming conventions, linting/PEP8, semantic markup, JS in separate files.  
- Security practices evidenced: env secrets, permissions, CSRF, DEBUG off.  
- Comprehensive testing with coverage; bugs documented with fixes or rationale.  
- Original implementation (not a walkthrough clone), UX rationale documented.  
- Configuration tidy, datastore settings centralised, branches managed well.

---

## 12) Accessibility Notes
- Use semantic tags (`header`, `nav`, `main`, `footer`, `section`, `h1‑h6`).  
- Provide alt text for images when you add them.  
- Ensure focus states and keyboard‑navigable menus.  
- Check colour contrast; test with Lighthouse and WAVE.

---

## 13) Backlog Ideas
- Availability calendar per Guide (grid).  
- Route detail pages with Leaflet map render of GPX.  
- Email notifications on booking/cancellation.  
- Guide role dashboards.  
- Pagination/filters/sorting on listings.

---

## 14) Credits & Plagiarism
- Attribute libraries, snippets, and assets.  
- Do not commit passwords or secret keys.  
- Rely on your own original code; when in doubt, cite sources.

---

## 15) Changelog Guidance
Keep a `CHANGELOG` section or use GitHub Releases to document feature increments mapped to user stories and acceptance criteria.
