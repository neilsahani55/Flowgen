# Flowgen

Flowgen is a Django 5 web application for AI-assisted content workflows.
It provides authenticated users with a central dashboard where they can
generate, analyze, and manage marketing content (blogs, landing pages,
comparisons, and customer rate reports). The admin interface is themed
with Jazzmin and aligned with Flowgen branding.

## Features

- Authentication: `register`, `login`, `logout`, `profile`
- Dashboard: `GET /content_dashboard/`
- Content Power:
  - UI: `GET /content_power/`
  - Webhook callback: `POST /content_power_api/` (stores content in cache by `session_id`)
  - Status polling: `GET /content_power_status/?session_id=...`
- Blog Generator:
  - UI: `GET /content_power/blog/`
  - Webhook callback: `POST /content_blog_api/` (stores blog data in cache by `job_id`)
  - Status polling: `GET /content_blog_status/?job_id=...`
- Landing Page Builder: `GET /content_power/landing_page/`
- Page Analysis: `GET /page_analysis/`
- n8n Integration: `GET /n8n_webhook/`
- Blog Viewer: `GET /blog/`
- Customer Rates Report: `GET /customer-rates/`

## Tech Stack

- Python 3.10+
- Django 5.2.5
- Jazzmin (admin UI theme)
- Requests, OpenPyXL
- SQLite (default)

## Project Layout

- `manage.py` – Django CLI entry
- `content_generations/` – project settings and URL routing
- `contentapp/` – main application (views, models, middleware, migrations)
- `templates/` – HTML templates (dashboard, blog, analysis, auth)
- `static/` – static assets

## Setup

1) Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
```

2) Install dependencies

```bash
pip install "Django==5.2.5" django-jazzmin requests openpyxl
```

3) Apply migrations

```bash
python manage.py migrate
```

4) Create an admin user (optional)

```bash
python manage.py createsuperuser
```

5) Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the app and `http://127.0.0.1:8000/admin/` for the Jazzmin-themed admin.
The Flowgen logo is served from `static/Gemini_Generated_Image_p859g5p859g5p859.svg`.

## Configuration

- `ALLOWED_HOSTS` is set in `content_generations/settings.py`. Update for your environment.
- `DEBUG` defaults to `True` for local development. Set to `False` for production.
- `SECRET_KEY` is currently hard-coded for development. In production, set it via an environment variable and load it securely.
- Static files:
  - Development: served from `static/`
  - Production: run `python manage.py collectstatic` and serve via your web server

## API Details

- `POST /content_power_api/`
  - Body: JSON with a `session_id` and content payload (flexible keys such as `content`, `output`, `result`, or `data`)
  - Effect: Stores the generated content in cache under `content_power_{session_id}`

- `GET /content_power_status/?session_id=...`
  - Response: JSON indicating `status` and `content` if available

- `POST /content_blog_api/`
  - Body: JSON or form-data with `job_id`, optional `html`, `meta_title`, `meta_description`, `image1`, `image2`, `image3`
  - Effect: Stores blog data in cache under `blog_job_{job_id}`

- `GET /content_blog_status/?job_id=...`
  - Response: JSON indicating `status` and `data` if available

## Development Notes

- Admin theme is configured via Jazzmin settings in `content_generations/settings.py` (Flowgen branding applied).
- The `contentapp/middleware.py` includes custom error handling and public route patterns.
- The `UserProfile` model is created automatically when a user is registered.

## Branding Guidelines

- Name: Flowgen (capitalize F, lowercase rest)
- Logo: `static/Gemini_Generated_Image_p859g5p859g5p859.svg`
- Primary Colors: `#0ea5e9` (sky blue), `#0284c7` (deep cyan)
- Secondary Colors: `#1e293b` (slate), `#64748b` (gray)
- Typography: Prefer system sans-serif stack (`'Segoe UI', Tahoma, Geneva, Verdana, sans-serif`)
- Usage:
  - Navbar and headers display “Flowgen” with the primary gradient.
  - Admin: Jazzmin `site_title`, `site_header`, `site_brand`, and `welcome_sign` use “Flowgen”.
  - Favicon and logos use the Flowgen SVG.
  - Avoid references to the former brand in new content; replace with Flowgen.

## Theme System

- Core variables live in templates and `static/css/effects.css`:
  - `--primary-gradient: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%)`
  - `--flowgen-primary: #0ea5e9`, `--flowgen-primary-2: #0284c7`
  - Focus ring and transition timing variables
- Primary buttons:
  - Use `.btn-primary` or `button[data-action="primary"]`
  - Effects include hover lift, active press, focus ring, and ripple
  - Disable ripple per-button with `data-ripple="false"`
- Updating theme:
  - Change colors by overriding CSS variables in `effects.css` and in template `:root` blocks
  - Adjust timing via `--btn-transition` (CSS) and `RIPPLE_MS` (JS)
  - Update any inline gradient styles to reference `--primary-gradient`
  - Keep accessibility by preserving `:focus-visible` styles

## Cross-Platform Consistency

- Web: Templates updated to display Flowgen name, logo, favicon, and colors.
- Mobile/Desktop: Use the same logo SVG (export PNG/ICO as needed), colors, and naming. Ensure app store listings and metadata use “Flowgen”.
- Marketing: Use the Flowgen name consistently in external docs, emails, and landing pages.

## Production Checklist

- Set `DEBUG=False` and configure `ALLOWED_HOSTS`.
- Provide a secure `SECRET_KEY` via environment variables.
- Configure a production-ready cache and database.
- Serve static files via a proper web server or CDN after `collectstatic`.
- Verify Flowgen branding across all pages and admin.

## License

Proprietary. All rights reserved.
