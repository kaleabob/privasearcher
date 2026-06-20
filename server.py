import json, os, re, time, urllib.request, urllib.error, warnings
warnings.filterwarnings('ignore')
from flask import Flask, jsonify, request, send_from_directory
from ddgs import DDGS

app = Flask(__name__, static_folder=None)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_TTL = 30
_search_cache = {}
SERPER_API_URL = "https://google.serper.dev/search"

def cache_response(key, loader):
    now = time.time()
    data = _search_cache.get(key)
    if data and now - data[0] < CACHE_TTL:
        return data[1]
    value = loader()
    _search_cache[key] = (now, value)
    return value


def query_serper(query, api_key):
    if not api_key:
        return None
    try:
        payload = json.dumps({"q": query, "source": "web", "hl": "en"}).encode("utf-8")
        req = urllib.request.Request(SERPER_API_URL, data=payload, headers={
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
        results = []
        for item in data.get("organic", []):
            results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", "")
            })
        return results
    except Exception:
        return None


def score_result(query, item):
    text = " ".join([str(item.get(k, "")) for k in ["title", "body", "snippet", "description", "source", "uploader"]]).lower()
    tokens = [t for t in re.split(r"\W+", query.lower()) if t]
    score = 0
    for token in tokens:
        if token in text:
            score += text.count(token) * 2
            if token in str(item.get("title", "")).lower():
                score += 3
    if query.lower() in text:
        score += 10
    return score


def normalize_results(results, query, mapper, max_items=20):
    seen = set()
    scored = []
    for r in results:
        item = mapper(r)
        if not item or not item.get("link"):
            continue
        link = item["link"]
        if link in seen:
            continue
        seen.add(link)
        item_score = score_result(query, r)
        item["score"] = item_score
        scored.append(item)
    scored.sort(key=lambda x: x["score"], reverse=True)
    output = []
    for item in scored[:max_items]:
        item.pop("score", None)
        output.append(item)
    return output


def extract_query_params(query):
    params = {}
    query_clean = query
    filetype_match = re.search(r'filetype:(\w+)', query)
    if filetype_match:
        params["filetype"] = filetype_match.group(1)
        query_clean = re.sub(r'filetype:\w+', '', query_clean)
    site_match = re.search(r'site:([^\s]+)', query)
    if site_match:
        params["site"] = site_match.group(1)
        query_clean = re.sub(r'site:[^\s]+', '', query_clean)
    return query_clean.strip(), params

@app.route("/health")
def health():
    return jsonify({"status": "ok", "timestamp": time.time()})

@app.route("/api/search")
def search_api():
    try:
        q = request.args.get("q", "").strip()
        if not q:
            return jsonify({"error": "Empty query"}), 400
        
        engine = request.args.get("engine", "duckduckgo")
        ss = request.args.get("ss", "off")
        sk = request.args.get("sk", "")
        
        cache_key = f"search:{engine}:{ss}:{q.lower()}"
        
        def search_impl():
            q_clean, params = extract_query_params(q)
            
            if engine == "google" and sk:
                results = query_serper(q_clean, sk)
                if results:
                    return {
                        "organic_results": normalize_results(results, q_clean, lambda x: x, 20),
                        "provider": "Google (Serper)"
                    }
            
            ddgs_kwargs = {"backend": "api"}
            if ss and ss != "off":
                ddgs_kwargs["safesearch"] = "on" if ss == "moderate" else "strict"
            
            if engine == "bing":
                results = DDGS(**ddgs_kwargs).text(q_clean, max_results=20, backend="bing")
            else:
                results = DDGS(**ddgs_kwargs).text(q_clean, max_results=20)
            
            mapper = lambda r: {"title": r.get("title", ""), "link": r.get("href", ""), "snippet": r.get("body", "")}
            return {
                "organic_results": normalize_results(results, q_clean, mapper, 20),
                "provider": f"{engine.title()} (DDGS)"
            }
        
        return jsonify(cache_response(cache_key, search_impl))
    except Exception as e:
        return jsonify({"error": str(e), "provider": "Error"}), 500

@app.route("/api/images")
def images_api():
    try:
        q = request.args.get("q", "").strip()
        if not q:
            return jsonify({"error": "Empty query"}), 400
        
        ss = request.args.get("ss", "off")
        cache_key = f"images:{ss}:{q.lower()}"
        
        def images_impl():
            ddgs_kwargs = {"backend": "api"}
            if ss and ss != "off":
                ddgs_kwargs["safesearch"] = "on" if ss == "moderate" else "strict"
            
            results = DDGS(**ddgs_kwargs).images(q, max_results=20)
            mapper = lambda r: {"title": r.get("title", ""), "link": r.get("url", ""), "imageUrl": r.get("image", "")}
            return {
                "organic_results": normalize_results(results, q, mapper, 20),
                "provider": "Images (DDGS)"
            }
        
        return jsonify(cache_response(cache_key, images_impl))
    except Exception as e:
        return jsonify({"error": str(e), "provider": "Error"}), 500

@app.route("/api/videos")
def videos_api():
    try:
        q = request.args.get("q", "").strip()
        if not q:
            return jsonify({"error": "Empty query"}), 400
        
        cache_key = f"videos:{q.lower()}"
        
        def videos_impl():
            results = DDGS().videos(q, max_results=20)
            mapper = lambda r: {
                "title": r.get("title", ""),
                "link": r.get("content", ""),
                "snippet": r.get("description", ""),
                "imageUrl": r.get("image", ""),
                "channel": r.get("source", ""),
                "duration": r.get("duration", "")
            }
            return {
                "organic_results": normalize_results(results, q, mapper, 20),
                "provider": "Videos (DDGS)"
            }
        
        return jsonify(cache_response(cache_key, videos_impl))
    except Exception as e:
        return jsonify({"error": str(e), "provider": "Error"}), 500

@app.route("/api/news")
def news_api():
    try:
        q = request.args.get("q", "").strip()
        if not q:
            return jsonify({"error": "Empty query"}), 400
        
        cache_key = f"news:{q.lower()}"
        
        def news_impl():
            results = DDGS().news(q, max_results=20)
            mapper = lambda r: {
                "title": r.get("title", ""),
                "link": r.get("url", ""),
                "snippet": r.get("body", ""),
                "imageUrl": r.get("image", ""),
                "source": r.get("source", ""),
                "date": r.get("date", "")
            }
            return {
                "organic_results": normalize_results(results, q, mapper, 20),
                "provider": "News (DDGS)"
            }
        
        return jsonify(cache_response(cache_key, news_impl))
    except Exception as e:
        return jsonify({"error": str(e), "provider": "Error"}), 500

@app.after_request
def apply_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,OPTIONS"
    return response

@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(BASE_DIR, path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    app.run(host="0.0.0.0", port=port, debug=False)
