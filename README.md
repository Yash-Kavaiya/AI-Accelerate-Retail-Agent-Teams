# AI-Accelerate-Retail-Agent-Teams

A sophisticated multi-agent retail system built with Google's Agent Development Kit (ADK), featuring specialized sub-agents for comprehensive retail operations.

Devpost:- https://devpost.com/software/ai-retail-agent-team-intelligent-retail-operations-platform
YouTube :- https://youtu.be/1_yr1BvFLCI?si=dmt0TqS2d_oAMVYt

## 🤖 Agent Architecture

<img width="1783" height="976" alt="image" src="https://github.com/user-attachments/assets/45e07284-f059-4f6d-ba2f-0d45d4b64825" />

This system implements a hierarchical multi-agent architecture with a coordinator agent managing five specialized sub-agents:

### Root Agent: Retail Coordinator
The main coordinator that routes customer requests to appropriate specialized agents and combines their outputs for comprehensive responses.

### Sub-Agents

#### 1. **Product Search Agent** 🔍
- Searches products by name, category, features, and price range
- Provides detailed product specifications and pricing
- Compares similar products
- Suggests alternatives for unavailable items
- Filters products by various criteria

<img width="640" height="350" alt="Product Search Agent" src="https://github.com/user-attachments/assets/2d3e25f7-a753-48c7-b336-b6b970f5a27b" />

#### 2. **Review Text Analysis Agent** 📊
- Analyzes customer reviews and extracts sentiment
- Identifies common themes and trends in reviews
- Summarizes product strengths and weaknesses
- Provides sentiment scores and ratings analysis
- Detects suspicious or fake reviews

<img width="640" height="350" alt="Review Text Analysis Agent" src="https://github.com/user-attachments/assets/9f3bc9a2-7f4e-43b4-9433-f10c60715fe7" />

#### 3. **Inventory Agent** 📦
- Checks real-time stock levels and availability
- Tracks inventory across multiple locations
- Provides low stock alerts and restock notifications
- Estimates delivery times based on inventory location
- Manages inventory reservations
<img width="640" height="350" alt="Inventory Agent" src="https://github.com/user-attachments/assets/673a96fa-7d82-497c-9c13-a9fbd9fdad25" />

#### 4. **Shopping Agent** 🛒
- Manages shopping cart operations
- Calculates totals including taxes and discounts
- Applies promotional codes and coupons
- Processes checkout and payment
- Provides order tracking information
- Suggests product bundles and upsells
<img width="640" height="350" alt="image" src="https://github.com/user-attachments/assets/e49e0b5b-5984-433e-ae70-06782ea277fe" />

#### 5. **Customer Support Agent** 💬
- Handles customer inquiries and issues
- Processes returns, refunds, and exchanges
- Tracks order status and shipping
- Resolves complaints professionally
- Provides warranty and product care information
- Escalates complex issues when needed

<img width="640" height="350" alt="image" src="https://github.com/user-attachments/assets/6e6af8fe-d1e2-4eff-b27d-ad94f81eb9a9" />

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Google ADK installed
- API keys configured

### Installation

1. Install dependencies:
```bash
pip install -r requirement.txt
```

2. Configure your environment:
   - Copy `retail-agents-team/.env.example` to `retail-agents-team/.env`
   - Add your API credentials to `.env`:

```bash
# Google AI Configuration
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=your_google_api_key_here

# Elasticsearch Configuration
ELASTICSEARCH_CLOUD_URL=your_elasticsearch_cloud_url_here
ELASTICSEARCH_API_KEY=your_elasticsearch_api_key_here
```

**⚠️ Security Note**: Never commit the `.env` file to version control. All credentials are now stored securely in environment variables.

### Running the Agent

#### Using ADK Web Interface
```bash
adk web retail-agents-team/
```

Then open your browser and interact with the retail coordinator agent.

#### Using ADK CLI
```bash
adk run retail-agents-team/
```

## 💡 Usage Examples

### Product Search
```
"Find me wireless headphones under $100"
"Compare iPhone 15 and Samsung Galaxy S24"
"Show me highly rated laptops for gaming"
```

### Review Analysis
```
"What are customers saying about the Sony WH-1000XM5?"
"Analyze recent reviews for product ID 12345"
"What are common complaints about this item?"
```

### Inventory Check
```
"Is the MacBook Pro in stock?"
"Check availability across all locations"
"When will item X be restocked?"
```

### Shopping Assistance
```
"Add 2 units of product Y to my cart"
"Apply coupon code SAVE20"
"Process checkout with express shipping"
```

### Customer Support
```
"I want to return my recent order"
"Track my order #12345"
"How do I exchange this item for a different size?"
```

## 🏗️ Project Structure

```
AI-Accelerate-Retail-Agent-Teams/
├── README.md                     # This file
├── requirement.txt               # Project dependencies
├── docs/                         # 📚 All documentation
│   ├── INDEX.md                 # Documentation index
│   ├── QUICKSTART.md            # Quick start guide
│   ├── SETUP.md                 # Setup instructions
│   ├── ARCHITECTURE.md          # System architecture
│   ├── AGENT_CONFIG.md          # Agent configuration
│   └── [agent-specific docs]   # Individual agent documentation
├── tests/                        # 🧪 Test files
│   ├── README.md                # Test documentation
│   ├── test_*_agent_tools.py   # Agent tests
│   └── test_*.py                # Infrastructure tests
├── retail-agents-team/          # 🤖 Agent implementations
│   ├── __init__.py
│   ├── agent.py                 # Multi-agent system definition
│   ├── customer_support_agent/
│   ├── inventory_agent/
│   ├── product_search_agent/
│   ├── review_text_analysis_agent/
│   └── shopping_agent/
└── ui/                          # 🖥️ User interface
    ├── index.html
    ├── server.py
    └── static/
```

## 📖 Documentation

All documentation is now organized in the `docs/` folder with comprehensive guides for each agent:

### 🚀 Getting Started
- **[Documentation Index](docs/INDEX.md)** - Complete documentation overview
- **[Quick Start Guide](docs/QUICKSTART.md)** - Get up and running quickly
- **[Setup Instructions](docs/SETUP.md)** - Detailed setup guide
- **[Architecture Overview](docs/ARCHITECTURE.md)** - System design and architecture
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Command shortcuts and tips

### 🤖 Agent Documentation (Detailed Guides)
Each agent has its own comprehensive documentation with tools, diagrams, examples, and best practices:

- **[🔍 Product Search Agent](docs/PRODUCT_SEARCH_AGENT.md)** - Text & image-based product search (8 tools)
- **[📊 Review Analysis Agent](docs/REVIEW_ANALYSIS_AGENT.md)** - Semantic review analysis with RRF (6 tools)
- **[📦 Inventory Agent](docs/INVENTORY_AGENT.md)** - Real-time inventory & demand forecasting (7 tools)
- **[🛒 Shopping Agent](docs/SHOPPING_AGENT.md)** - Customer behavior & transaction analytics (7 tools)
- **[💬 Customer Support Agent](docs/CUSTOMER_SUPPORT_AGENT.md)** - FAQ-based support system (5 tools)

## 🛠️ Technology Stack

- **Framework**: Google Agent Development Kit (ADK)
- **LLM Model**: Gemini 2.0 Flash
- **Architecture**: Multi-agent hierarchical system
- **Language**: Python

## 📚 Agent Coordination

The system uses ADK's native orchestration capabilities:
- The root agent intelligently routes requests to specialized agents
- Multiple agents can work in parallel for complex requests
- Context is maintained across agent handoffs
- Responses are consolidated for a unified customer experience

<img width="3022" height="697" alt="image" src="https://github.com/user-attachments/assets/08933297-96fd-4273-a29c-3be4611fb9d3" />

## 🔧 Customization

Each agent can be customized by modifying their:
- `instruction`: Define agent behavior and responsibilities
- `description`: Specify agent expertise
- `tools`: Add custom tools for extended functionality (coming soon)

## 🧪 Testing

All test files are organized in the `tests/` directory. See [tests/README.md](tests/README.md) for detailed testing instructions.

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_customer_support_agent_tools.py
```
<img width="1772" height="639" alt="image" src="https://github.com/user-attachments/assets/00d97a83-f094-4121-9e7f-15d3273decf6" />

<img width="933" height="373" alt="image" src="https://github.com/user-attachments/assets/e25692a6-9236-4035-814e-c8504dbbc72d" />

## 📝 License

This project is built using Google's ADK framework.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 📞 Support

For issues or questions, please open an issue in the repository.

---

**Note**: This project has been reorganized for better structure. See [docs/PROJECT_REORGANIZATION.md](docs/PROJECT_REORGANIZATION.md) for details on the new organization.
