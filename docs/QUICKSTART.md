# Quick Start Guide - Retail Agent Team

## 🚀 Getting Started in 5 Minutes

### Prerequisites
- Python 3.8 or higher
- Google ADK installed
- Google API Key

### Installation Steps

#### 1. Install Dependencies
```bash
cd AI-Accelerate-Retail-Agent-Teams
pip install -r requirement.txt
```

#### 2. Configure Environment
```bash
# Copy the example env file
copy .env.example .env

# Edit .env and add your API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

#### 3. Verify Installation
```bash
# Check ADK installation
adk --version

# Validate agent configuration
adk validate retail-agents-team/
```

#### 4. Run the Agent System
```bash
# Start the web interface
adk web retail-agents-team/
```

The web interface will open at `http://localhost:8000`

### First Interactions

Try these example queries:

#### Product Search
```
"Find wireless headphones under $100"
```
Expected: product_search_agent will respond with matching products

#### Review Analysis
```
"What are customers saying about Sony WH-1000XM5?"
```
Expected: review_text_analysis_agent will analyze reviews

#### Inventory Check
```
"Is the MacBook Pro in stock?"
```
Expected: inventory_agent will check availability

#### Shopping
```
"Add 2 wireless mice to my cart"
```
Expected: shopping_agent will update cart

#### Customer Support
```
"I want to return my recent order"
```
Expected: customer_support_agent will help with returns

## 📂 Project Structure

```
AI-Accelerate-Retail-Agent-Teams/
│
├── retail-agents-team/              # Main agent directory
│   ├── agent.py                     # Root coordinator
│   ├── product_search_agent/        # Product search module
│   ├── review_text_analysis_agent/  # Review analysis module
│   ├── inventory_agent/             # Inventory module
│   ├── shopping_agent/              # Shopping module
│   └── customer_support_agent/      # Support module
│
├── README.md                        # Project overview
├── ARCHITECTURE.md                  # Architecture documentation
├── AGENT_CONFIG.md                  # Agent configuration details
├── requirement.txt                  # Python dependencies
└── .env.example                     # Environment template
```

## 🧪 Testing Individual Agents

### Test Product Search Agent
```bash
adk run retail-agents-team/product_search_agent/
```

### Test Review Analysis Agent
```bash
adk run retail-agents-team/review_text_analysis_agent/
```

### Test Inventory Agent
```bash
adk run retail-agents-team/inventory_agent/
```

### Test Shopping Agent
```bash
adk run retail-agents-team/shopping_agent/
```

### Test Customer Support Agent
```bash
adk run retail-agents-team/customer_support_agent/
```

## 🔧 Common Commands

### Development
```bash
# Run with auto-reload
adk web retail-agents-team/ --reload

# Run in debug mode
adk run retail-agents-team/ --debug
```

### Testing
```bash
# Run with test input
adk run retail-agents-team/ --replay test_input.json

# Validate configuration
adk validate retail-agents-team/
```

### Deployment
```bash
# Build for production
adk build retail-agents-team/

# Deploy to Cloud Run
adk deploy retail-agents-team/
```

## 💡 Example Workflows

### Workflow 1: Product Discovery
```
User: "Find gaming laptops under $1500 with good reviews"

Process:
1. Coordinator routes to product_search_agent
2. product_search_agent finds matching laptops
3. Coordinator routes to review_text_analysis_agent
4. review_text_analysis_agent analyzes reviews
5. Coordinator synthesizes and presents results
```

### Workflow 2: Purchase Flow
```
User: "I want to buy the Dell XPS 15"

Process:
1. Coordinator routes to product_search_agent (find product)
2. Coordinator routes to inventory_agent (check stock)
3. Coordinator routes to shopping_agent (add to cart)
4. shopping_agent guides through checkout
```

### Workflow 3: Post-Purchase Support
```
User: "Track my order #12345"

Process:
1. Coordinator routes to customer_support_agent
2. customer_support_agent looks up order
3. Returns tracking information and status
```

## 🐛 Troubleshooting

### Issue: "API Key not found"
**Solution**: 
```bash
# Set environment variable directly
set GOOGLE_API_KEY=your_key_here  # Windows
export GOOGLE_API_KEY=your_key_here  # Linux/Mac
```

### Issue: "Agent not found"
**Solution**: Check that all `__init__.py` files exist in agent folders

### Issue: "Import error"
**Solution**: Ensure you're running from project root directory
```bash
cd AI-Accelerate-Retail-Agent-Teams
adk web retail-agents-team/
```

### Issue: "Slow responses"
**Solution**: 
- Check internet connection
- Verify API rate limits
- Consider using gemini-2.0-flash for faster responses

## 📚 Learning Resources

### ADK Documentation
- [Google ADK Python Docs](https://github.com/google/adk-python)
- [Multi-Agent Systems](https://github.com/google/adk-python#multi-agent)
- [Agent Configuration](https://github.com/google/adk-python#configuration)

### Project Documentation
- `ARCHITECTURE.md` - System architecture details
- `AGENT_CONFIG.md` - Agent configuration reference
- `README.md` - Project overview

## 🎯 Next Steps

### Immediate
1. ✅ Install and configure environment
2. ✅ Run the agent system
3. ✅ Try example queries
4. ✅ Test individual agents

### Short Term
1. Customize agent instructions
2. Add custom tools (when available)
3. Integrate with real databases
4. Add authentication

### Long Term
1. Deploy to production
2. Monitor and optimize performance
3. Add new specialized agents
4. Integrate with existing systems

## 🤝 Getting Help

### Documentation
- Read `ARCHITECTURE.md` for system design
- Check `AGENT_CONFIG.md` for configuration options
- Review example queries in `README.md`

### Debugging
```bash
# Check agent configuration
adk validate retail-agents-team/

# View detailed logs
adk run retail-agents-team/ --log-level DEBUG

# Test with sample input
adk run retail-agents-team/ --replay input.json
```

### Community
- GitHub Issues: Report bugs or request features
- Discussions: Ask questions and share ideas

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] ADK package installed (`pip install google-adk`)
- [ ] API key configured in `.env`
- [ ] All agent folders have `__init__.py` and `agent.py`
- [ ] Can run `adk validate retail-agents-team/` successfully
- [ ] Web interface opens at `http://localhost:8000`
- [ ] Test queries work correctly

## 🎉 Success!

If you've reached this point, your retail agent team is ready to use!

Try a complex query:
```
"Find me a laptop under $1200 that has great reviews, 
is in stock, and can be delivered by next week"
```

Watch as the coordinator orchestrates multiple agents to provide a comprehensive answer!
