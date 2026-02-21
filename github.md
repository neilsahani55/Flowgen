# Publishing Flowgen to GitHub

This guide explains how to prepare the Flowgen project for GitHub, which
files to include or ignore, and how to push to a new GitHub repository.

---

## 1. Prerequisites

- Git installed on your machine
- GitHub account
- This project checked out at:
  `C:\Users\Graphic\Documents\content_generations`

---

## 2. Sensitive Data & Webhooks

Before publishing the project publicly:

- Rotate and/or remove any production secrets that already exist in the
  repository:
  - Django `SECRET_KEY` (now loaded from `DJANGO_SECRET_KEY` env var)
  - Provider API tokens for customer rates (configure via environment
    variables or an external config rather than hard-coding real tokens)
- If you keep this repository public:
  - Use placeholder values for example tokens and document how to supply
    real values via environment variables.
  - Treat any real tokens already committed as compromised and rotate
    them in the provider dashboards.

Webhook URLs used by the frontend (for blog generation, comparison,
page analysis, etc.) are currently visible in templates. If these
webhooks are security-sensitive, consider:

- Moving them behind your own backend endpoints, or
- Using separate “public” n8n workflows that accept only safe payloads.

---

## 3. Files and Folders to Include

From the project root, the core items to track in Git:

- `manage.py`
- `content_generations/` (project settings, URLs, ASGI/WSGI)
- `contentapp/` (views, models, middleware, migrations, tests)
- `templates/` (all HTML files)
- `static/` (CSS, JS, images)
- `README.md`
- `CHANGELOG.md`
- `github.md` (this guide)

These are the source code, configuration, and documentation required to
run and understand the project.

---

## 4. Files and Folders to Exclude (.gitignore)

Create a `.gitignore` in the project root (already provided in this
repository). It should ignore:

- Python cache and build artifacts:
  - `__pycache__/`
  - `*.py[cod]`
  - `*.pyo`
  - `*.pyd`
  - `*.egg-info/`
  - `dist/`
  - `build/`
- Virtual environments:
  - `.venv/`
  - `venv/`
- Local environment/config:
  - `.env`
  - `.env.*`
- Local databases and development files:
  - `db.sqlite3`
  - `*.sqlite3`
  - `nohup.out`
  - Any temporary files or logs you generate locally

When using GitHub, everything not ignored by `.gitignore` will be
uploaded, so ensure secrets and large transient files are covered.

---

## 5. Initialize Git (if not already initialized)

From the project root:

```bash
cd C:\Users\Graphic\Documents\content_generations
git init
```

Confirm Git sees your files:

```bash
git status
```

You should see project files listed as “untracked”.

---

## 6. First Commit

Stage all tracked files except those ignored by `.gitignore`:

```bash
git add .
```

Verify what will be committed:

```bash
git status
```

Then create an initial commit:

```bash
git commit -m "Initial commit: Flowgen Django application"
```

---

## 7. Create a GitHub Repository

1. Log in to GitHub.
2. Click **New** repository.
3. Choose a name, for example `flowgen`.
4. Set visibility:
   - **Private** if you plan to keep secrets (recommended), or
   - **Public** after scrubbing secrets as described above.
5. Do **not** initialize with a README or .gitignore (you already have
   them locally).

GitHub will show you a remote URL like:

```text
https://github.com/<your-username>/flowgen.git
```

---

## 8. Add Remote and Push

Back in your terminal:

```bash
cd C:\Users\Graphic\Documents\content_generations
git remote add origin https://github.com/<your-username>/flowgen.git
git branch -M main
git push -u origin main
```

Replace `<your-username>` with your GitHub username.

After this, your project will be available on GitHub. Future changes can
be committed and pushed with:

```bash
git add .
git commit -m "Describe your change"
git push
```

---

## 9. Recommended Additional Steps

- Create a `.env` file locally (not committed) for:
  - `DJANGO_SECRET_KEY`
  - Any provider API tokens
  - Any other secret configuration values
- Document all required environment variables in the README or in a
  separate `ENVIRONMENT.md` if needed.
- If you use GitHub Actions or other CI, store secrets in the platform’s
  secret store rather than in the repository.

