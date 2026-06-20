# privasearcher
PrivaSearch is a privacy-focused web search interface with a Flask backend and a client-side browser shell.

## Features
- Search results via DuckDuckGo + optional Google/Serper fallback
- Images, videos, and news search APIs
- Local tabbed browser UI with a homepage and shortcuts
- Private AI assistant interface (`Privo`)
- Render-ready deployment with `gunicorn`

## Deploy on Render
1. Create a Render account and connect your GitHub repository.
2. Add `render.yaml` to the repo.
3. Configure a secret named `SERPER_API_KEY` if you want Google/Serper results.
4. Deploy the `main` branch.

## Deploy on GitHub Pages
1. Push this repository to GitHub.
2. Enable GitHub Pages in the repository settings and set it to use the `gh-pages` branch and root `/` directory.
3. The workflow file `.github/workflows/deploy-pages.yml` will publish the static homepage automatically on every push to `main`.
4. Note: `index.html` is a static landing page. The actual search interface in `app.html` still requires a backend API.
5. To connect `app.html` from GitHub Pages to a hosted backend, open it with `?api_base=https://your-backend.example.com`.

## Run locally
```bash
python3 -m pip install -r requirements.txt
python3 server.py
```

Then open `http://127.0.0.1:8888` in your browser.
