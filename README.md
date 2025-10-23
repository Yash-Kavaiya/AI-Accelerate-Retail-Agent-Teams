# AI-Accelerate-Retail-Agent-Teams

A sophisticated multi-agent retail system built with Google's Agent Development Kit (ADK), featuring specialized sub-agents for comprehensive retail operations.

## 🤖 Agent Architecture

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

#### 2. **Review Text Analysis Agent** 📊
- Analyzes customer reviews and extracts sentiment
- Identifies common themes and trends in reviews
- Summarizes product strengths and weaknesses
- Provides sentiment scores and ratings analysis
- Detects suspicious or fake reviews

#### 3. **Inventory Agent** 📦
- Checks real-time stock levels and availability
- Tracks inventory across multiple locations
- Provides low stock alerts and restock notifications
- Estimates delivery times based on inventory location
- Manages inventory reservations

#### 4. **Shopping Agent** 🛒
- Manages shopping cart operations
- Calculates totals including taxes and discounts
- Applies promotional codes and coupons
- Processes checkout and payment
- Provides order tracking information
- Suggests product bundles and upsells

#### 5. **Customer Support Agent** 💬
- Handles customer inquiries and issues
- Processes returns, refunds, and exchanges
- Tracks order status and shipping
- Resolves complaints professionally
- Provides warranty and product care information
- Escalates complex issues when needed

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
```bash
# Set your Google API key
export GOOGLE_API_KEY=your_api_key_here
```

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
├── README.md
├── requirement.txt
└── retail-agents-team/
    ├── __init__.py
    └── agent.py          # Multi-agent system definition
```

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

## 🔧 Customization

Each agent can be customized by modifying their:
- `instruction`: Define agent behavior and responsibilities
- `description`: Specify agent expertise
- `tools`: Add custom tools for extended functionality (coming soon)

## 📝 License

This project is built using Google's ADK framework.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 📞 Support

For issues or questions, please open an issue in the repository.