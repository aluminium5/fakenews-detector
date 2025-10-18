# Deploying FakeNews-Detector to Railway

This file contains quick steps to deploy the backend and UI on Railway using the `deploy-prep` branch. I prepared a `deploy-prep` branch with small, safe changes (PORT handling, Procfile, requirements, and a Windows-friendly `run_prod.py`) so you can deploy quickly without breaking the working state.

Quick summary
- Backend: `fakenews-backend/` — Python Flask app. Uses `Procfile` and `fakenews-backend/requirements.txt`.
- UI: `fake-news-ui/fake-news-ui/` — Rocket (Rust) app. Deploy as a separate service or with Docker.

1) Push branch (already prepared locally)

If the branch isn't pushed yet, run:

```powershell
git push origin deploy-prep
```

2) Create the backend service on Railway

- In Railway, create a new project and choose "Deploy from GitHub" or connect your repo.
- Choose the `deploy-prep` branch.
- Set the service root to `fakenews-backend/`.
- Railway will detect `requirements.txt`. If not, set the build command to:

  pip install -r requirements.txt

- Start command (Procfile is present, Railway will use it). If Railway needs a direct command, use:

  gunicorn -w 4 -b 0.0.0.0:$PORT app:app

- Add environment variables (if any). For local testing this isn't required. For production you may want to set a restricted CORS origin.

3) Create the UI service on Railway

- Create a second Railway service (same repo) and set the root to `fake-news-ui/fake-news-ui/`.
- If Railway supports Rust builds directly, it will run `cargo build --release`. If not, use a Dockerfile.
- Set an environment variable for backend URL so the UI knows where to send requests, e.g. `BACKEND_URL` = `https://<your-backend>.railway.app`.

4) Model artifacts

- Two options:
  - Commit `fakenews-backend/model.pkl` and `vectorizer.pkl` into the backend folder (already present). This is simplest, but increases repo size.
  - Better for production: host artifacts in S3 (or Railway volumes) and download them at startup. If you keep them committed, ensure they are in the backend folder and `app.py` loads them relative to the module directory.

5) Run locally (quick smoke test)

From `fakenews-backend/` with an active venv:

```powershell
# Install deps
.\venv\Scripts\python.exe -m pip install -r requirements.txt

# Run locally with Waitress (Windows-friendly, included in requirements):
.\venv\Scripts\python.exe run_prod.py

# Or run with gunicorn (Linux/CI):
.\venv\Scripts\python.exe -m gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Smoke test:
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/predict -ContentType 'application/json' -Body (@{text='smoke test'} | ConvertTo-Json)
```

6) Rollback / safety

- If anything goes wrong on Railway, you can switch the deployment back to the `main` branch or redeploy the previous release via Railway UI.

7) Notes & follow-ups (recommended)
- Remove committed `venv/` from repo (I added `.gitignore`; I did not force-delete files on disk). Run `git rm -r --cached fakenews-backend/venv` then commit.
- Consider hosting large model files in S3 and downloading at startup for repeatable deploys.
- Tighten CORS policy before public launch.

If you'd like, I can push the `deploy-prep` branch now and configure the repo on Railway for you (I will not change `main`). Say "push branch and add README" and I'll push and report the remote URL and next steps.
