# Quick Reference Guide

## 🗂️ File Organization

### Root Directory (Production Files Only)
```
AI-Accelerate-Retail-Agent-Teams/
├── README.md           # Start here!
├── requirement.txt     # Install: pip install -r requirement.txt
├── docs/              # 📚 All documentation
├── tests/             # 🧪 All tests
├── retail-agents-team/ # 🤖 Agent code (production)
└── ui/                # 🖥️ Web interface (production)
```

## 🚀 Quick Commands

### Setup
```bash
# Install dependencies
pip install -r requirement.txt

# Configure API key (required)
$env:GOOGLE_API_KEY="your_api_key_here"
```

### Run the Application
```bash
# Start with web interface
adk web retail-agents-team/

# Or use CLI
adk run retail-agents-team/
```

### Run Tests
```bash
# All tests
pytest tests/

# Specific test
pytest tests/test_shopping_agent_tools.py

# With coverage
pytest --cov=retail-agents-team tests/
```

### Run UI Server
```bash
cd ui
python server.py
# Then open http://localhost:5000
```

## 📖 Documentation Shortcuts

| What you need | Where to look |
|---------------|---------------|
| Getting started | [docs/QUICKSTART.md](docs/QUICKSTART.md) |
| Setup guide | [docs/SETUP.md](docs/SETUP.md) |
| Architecture | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| All docs | [docs/INDEX.md](docs/INDEX.md) |
| Test info | [tests/README.md](tests/README.md) |

## 🤖 Agent Information

| Agent | Purpose | Documentation |
|-------|---------|---------------|
| Product Search | Find products | [docs/product_search_agent_README.md](docs/product_search_agent_README.md) |
| Review Analysis | Analyze reviews | [docs/review_text_analysis_agent_README.md](docs/review_text_analysis_agent_README.md) |
| Inventory | Check stock | [docs/inventory_agent_README.md](docs/inventory_agent_README.md) |
| Shopping | Cart & checkout | [docs/SHOPPING_AGENT_SETUP_COMPLETE.md](docs/SHOPPING_AGENT_SETUP_COMPLETE.md) |
| Customer Support | Help customers | [docs/customer_support_agent_README.md](docs/customer_support_agent_README.md) |

## 📁 What's in Each Folder?

### `docs/` (18 files)
- Complete documentation
- Setup guides
- Architecture docs
- Agent-specific guides

### `tests/` (7 files + README)
- Unit tests for all agents
- Integration tests
- Test utilities

### `retail-agents-team/`
- Main agent orchestrator
- 5 specialized agent folders
- Production Python code

### `ui/`
- Web interface
- HTML/CSS/JS files
- Flask server

## 🎯 Common Tasks

### Adding a New Feature
1. Edit agent code in `retail-agents-team/`
2. Add tests in `tests/`
3. Update docs in `docs/`

### Running in Production
Only deploy these folders:
- `retail-agents-team/`
- `ui/`
- `requirement.txt`
- `README.md`

### Development Setup
```bash
# 1. Clone repo
# 2. Install dependencies
pip install -r requirement.txt

# 3. Set environment variables
$env:GOOGLE_API_KEY="your_key"

# 4. Run tests to verify
pytest tests/

# 5. Start development
adk web retail-agents-team/
```

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Import errors | Run `pip install -r requirement.txt` |
| API errors | Check `GOOGLE_API_KEY` is set |
| Test failures | See `tests/README.md` for setup |
| Agent not responding | Check `docs/SETUP.md` for configuration |

## 📞 Need Help?

1. Check [docs/INDEX.md](docs/INDEX.md) for all documentation
2. Review [docs/QUICKSTART.md](docs/QUICKSTART.md) for quick setup
3. See [docs/SETUP.md](docs/SETUP.md) for detailed configuration
4. Check [tests/README.md](tests/README.md) for testing info
5. Open an issue on GitHub

---

**Pro Tip**: Bookmark this file for quick reference! 🔖
