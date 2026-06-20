# ✨ PrivaSearch - Privacy-First Meta Search Engine

> A completely private, ad-free search engine with AI summaries, tab-based browsing, and advanced search features.

## 🌟 Core Features

### Search Capabilities
- **Multi-Engine Support**: DuckDuckGo, Bing, Google (via Serper API)
- **Content Types**: Web search, Images, Videos, News
- **Smart Ranking**: Token-based relevance scoring for better results
- **Advanced Operators**: 
  - `site:example.com` - Search specific domains
  - `filetype:pdf` - Find specific file types
  - `"exact phrase"` - Match exact phrases
  - `-word` - Exclude words from results
- **Safe Search**: Off/Moderate/Strict content filtering
- **Caching**: 30-second cache prevents API rate limiting

### User Interface
- **Beautiful Homepage**: Modern gradient design with 12 quick shortcuts
- **Tab-Based Browser**: Open multiple tabs for browsing
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark Mode**: Eye-friendly interface

### AI Features
- **AI Overviews**: Auto-generated summaries of search results
- **Privo Chat**: Conversational AI assistant with image support
- **Multiple AI Models**: 
  - GPT-4o, Mistral, DeepSeek, Claude (free via Pollinations)
  - Premium models via OpenRouter

### Browser Capabilities
- **Proxy Bypass**: Secure browsing via iframe proxy
- **History Stack**: Back/Forward navigation
- **Related Searches**: Contextual suggestions below results
- **Keyboard Shortcuts**: Full keyboard navigation support

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python3 server.py

# Visit http://localhost:8888
```

### Deploy on Render
1. Connect your GitHub repo to Render
2. Create a new Web Service
3. Select Python environment
4. Add secret `SERPER_API_KEY` (optional, from serper.dev)
5. Deploy!

### Production with Gunicorn
```bash
gunicorn server:app --bind 0.0.0.0:8000 --workers 4
```

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+T` | New tab |
| `Ctrl+W` | Close current tab |
| `Ctrl+K` or `Ctrl+L` | Focus search box |
| `Alt+←` | Go back |
| `Alt+→` | Go forward |
| `?` | Show help |
| `Enter` | Search |

## 📊 API Endpoints

### Search
```
GET /api/search?q=<query>&engine=<engine>&ss=<level>&sk=<key>
```
- `q` - Search query (required)
- `engine` - duckduckgo, bing, or google (default: duckduckgo)
- `ss` - Safe search level: off, moderate, strict (default: off)
- `sk` - Serper API key for Google results (optional)

### Images
```
GET /api/images?q=<query>&ss=<level>
```

### Videos
```
GET /api/videos?q=<query>
```

### News
```
GET /api/news?q=<query>
```

### Health Check
```
GET /health
```
Returns `{"status": "ok", "timestamp": <unix_timestamp>}`

## ⚙️ Configuration

### Environment Variables
- `PORT` - Server port (default: 8888)
- `SERPER_API_KEY` - API key for Google results (optional)

### Settings Modal (⚙️ icon)
- **Search Engine**: Choose default search engine
- **Safe Search**: Content filtering level
- **AI Model**: Select AI provider
- **API Keys**: Add Serper or OpenRouter keys

## 🎯 Advanced Features

### Smart Result Ranking
- Title matches scored higher than snippet matches
- Exact phrase matches get bonus points
- Duplicate results removed automatically

### Related Searches
Auto-generated suggestions based on:
- Query keywords
- Common search patterns
- Result analysis

### AI Summaries
- Concise, factual overview of top results
- HTML-formatted with structured content
- Generates in ~600ms for quick display

## 🔒 Privacy & Security

- **No Tracking**: No user analytics or cookies
- **No Ads**: Completely ad-free
- **Private Searches**: All searches are anonymous
- **Secure Proxy**: Optional iframe-based proxy for website browsing
- **Open Source**: Fully transparent codebase

## 📦 Technology Stack

### Backend
- **Flask 3.1.3** - Web framework
- **DDGS 9.14.4** - DuckDuckGo search library
- **Serper API** - Optional Google search (requires API key)
- **Gunicorn 23.0.0** - Production WSGI server

### Frontend
- **Vanilla JavaScript** - No frameworks, pure JS
- **HTML5 & CSS3** - Modern web standards
- **Font Awesome** - Icon library
- **Google Fonts** - Typography

### Deployment
- **Render.com** - Primary deployment platform
- **Docker** - Container support
- **Environment Config** - 12-factor app compliant

## 📋 File Structure

```
privasearcher/
├── server.py           # Flask backend with API routes
├── index.html          # Single-page app frontend
├── requirements.txt    # Python dependencies
├── Procfile           # Heroku deployment config
├── render.yaml        # Render production config
├── render.local.yaml  # Render local testing config
└── README.md          # Documentation
```

## 🔧 Development

### Running Tests
```bash
# Syntax check
python3 -m py_compile server.py

# API test
curl http://localhost:8888/health
```

### Adding Features
1. Backend changes in `server.py`
2. Frontend changes in `index.html`
3. Update `requirements.txt` if new dependencies
4. Test locally before deploying

## 📈 Performance

- **Caching**: 30-second TTL reduces API calls
- **Result Deduplication**: Removes duplicate URLs
- **Smart Ranking**: Fast relevance scoring
- **Lazy Loading**: Images load on demand

## 🐛 Troubleshooting

### No search results
- Check internet connection
- Verify DDGS is accessible
- Check browser console for errors
- Try a different search engine

### API timeout
- Search query might be too broad
- DuckDuckGo might be rate limiting
- Try with safe search enabled

### Render deployment fails
- Check Python version in build logs
- Verify `requirements.txt` is correct
- Check for syntax errors: `python3 -m py_compile server.py`

## 📞 Support

Issues? Check the browser console (F12) for error details.

## 📄 License

Open source and free to use, modify, and deploy.

---

**Built with ❤️ for privacy**
