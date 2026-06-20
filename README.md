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

## Run locally
```bash
python3 -m pip install -r requirements.txt
python3 server.py
```

Then open `http://127.0.0.1:8888` in your browser.
