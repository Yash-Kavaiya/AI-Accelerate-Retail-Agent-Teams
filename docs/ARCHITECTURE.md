# Retail Agent Team - Modular Architecture

## 📁 Project Structure

```
AI-Accelerate-Retail-Agent-Teams/
├── README.md
├── requirement.txt
├── .env.example
└── retail-agents-team/
    ├── __init__.py
    ├── agent.py                              # Root coordinator agent
    │
    ├── product_search_agent/
    │   ├── __init__.py
    │   └── agent.py                          # Product search specialist
    │
    ├── review_text_analysis_agent/
    │   ├── __init__.py
    │   └── agent.py                          # Review analysis specialist
    │
    ├── inventory_agent/
    │   ├── __init__.py
    │   └── agent.py                          # Inventory management specialist
    │
    ├── shopping_agent/
    │   ├── __init__.py
    │   └── agent.py                          # Shopping cart & checkout specialist
    │
    └── customer_support_agent/
        ├── __init__.py
        └── agent.py                          # Customer support specialist
```

## 🏗️ Architecture Overview

### Modular Design Principles

1. **Separation of Concerns**: Each agent is in its own folder with dedicated responsibilities
2. **Single Responsibility**: Each agent focuses on one domain of retail operations
3. **Hierarchical Structure**: Root coordinator manages specialized sub-agents
4. **Scalability**: Easy to add new agents or modify existing ones
5. **Maintainability**: Changes to one agent don't affect others

### Agent Hierarchy

```
retail_coordinator (Root Agent)
├── product_search_agent
├── review_text_analysis_agent
├── inventory_agent
├── shopping_agent
└── customer_support_agent
```

## 🤖 Agent Modules

### 1. Root Coordinator (`retail-agents-team/agent.py`)

**Responsibility**: Orchestrates all sub-agents and manages complex workflows

**Key Functions**:
- Intelligent request routing to appropriate agents
- Multi-agent coordination for complex queries
- Context management across agent interactions
- Response synthesis from multiple agents

### 2. Product Search Agent (`product_search_agent/`)

**Responsibility**: Product discovery and information

**Key Functions**:
- Search products by various criteria
- Filter and compare products
- Provide detailed specifications
- Suggest alternatives

**Use Cases**:
- "Find wireless headphones under $100"
- "Compare iPhone 15 vs Samsung Galaxy S24"
- "Show me gaming laptops with RTX 4080"

### 3. Review Text Analysis Agent (`review_text_analysis_agent/`)

**Responsibility**: Customer review analysis and insights

**Key Functions**:
- Sentiment analysis
- Theme extraction
- Product strength/weakness identification
- Fake review detection

**Use Cases**:
- "What are customers saying about this product?"
- "Analyze recent reviews for product X"
- "Summarize pros and cons from reviews"

### 4. Inventory Agent (`inventory_agent/`)

**Responsibility**: Stock management and availability tracking

**Key Functions**:
- Real-time stock checks
- Multi-location inventory tracking
- Delivery time estimation
- Restock notifications

**Use Cases**:
- "Is the MacBook Pro in stock?"
- "Check availability across all warehouses"
- "When will this item be restocked?"

### 5. Shopping Agent (`shopping_agent/`)

**Responsibility**: Cart management and checkout processing

**Key Functions**:
- Cart operations (add/remove/update)
- Price calculation with taxes and discounts
- Coupon application
- Checkout processing

**Use Cases**:
- "Add 2 items to my cart"
- "Apply coupon SAVE20"
- "Calculate shipping to New York"

### 6. Customer Support Agent (`customer_support_agent/`)

**Responsibility**: Customer service and issue resolution

**Key Functions**:
- Order tracking and inquiries
- Returns and refunds processing
- Policy information
- Complaint resolution

**Use Cases**:
- "Track my order #12345"
- "I want to return my purchase"
- "What's your return policy?"

## 🔄 Agent Interaction Patterns

### Single-Agent Flow
```
Customer Query → Coordinator → Specialized Agent → Response
```

Example: "What's the return policy?" → customer_support_agent

### Multi-Agent Sequential Flow
```
Customer Query → Coordinator → Agent 1 → Agent 2 → Combined Response
```

Example: "Find laptops under $1000 that are in stock"
- product_search_agent (finds laptops)
- inventory_agent (checks stock)

### Multi-Agent Parallel Flow
```
Customer Query → Coordinator → [Agent 1, Agent 2, Agent 3] → Synthesized Response
```

Example: "I want to buy a highly-rated camera that's in stock"
- product_search_agent (finds cameras)
- review_text_analysis_agent (analyzes ratings)
- inventory_agent (checks availability)

## 🛠️ Customization Guide

### Adding a New Agent

1. Create a new folder in `retail-agents-team/`:
```bash
mkdir retail-agents-team/new_agent_name
```

2. Create `__init__.py`:
```python
from . import agent
```

3. Create `agent.py`:
```python
from google.adk.agents import Agent

root_agent = Agent(
    name='new_agent_name',
    model='gemini-2.0-flash',
    description='Agent description',
    instruction='Detailed instructions...'
)
```

4. Import in main `agent.py`:
```python
from .new_agent_name.agent import root_agent as new_agent_name
```

5. Add to sub_agents list:
```python
sub_agents=[
    # existing agents...
    new_agent_name
]
```

### Modifying an Agent

Each agent can be modified independently:
- Update instructions in `agent.py`
- Add tools (when available)
- Adjust model parameters
- Enhance descriptions

### Adding Tools to Agents

When tools are needed (future enhancement):

```python
from google.adk.agents import Agent
from google.adk.tools import custom_tool

root_agent = Agent(
    name='agent_name',
    model='gemini-2.0-flash',
    description='...',
    instruction='...',
    tools=[custom_tool]  # Add tools here
)
```

## 🚀 Running the Agents

### Individual Agent Testing

Test a single agent:
```bash
adk run retail-agents-team/product_search_agent/
```

### Full System

Run the complete multi-agent system:
```bash
adk web retail-agents-team/
```

### Development Mode

For local development:
```bash
adk run retail-agents-team/ --reload
```

## 📊 Benefits of Modular Architecture

1. **Maintainability**: 
   - Easy to update individual agents
   - Changes are isolated to specific modules
   - Clear code organization

2. **Scalability**:
   - Add new agents without affecting existing ones
   - Scale individual agents based on load
   - Parallel development by different teams

3. **Testability**:
   - Test each agent independently
   - Mock sub-agents for integration testing
   - Clear interfaces between components

4. **Reusability**:
   - Agents can be used in different contexts
   - Share common agent patterns
   - Extract and reuse agent logic

5. **Flexibility**:
   - Swap out agent implementations
   - A/B test different agent configurations
   - Mix and match agents for different use cases

## 🔍 Debugging Tips

### Test Individual Agents
```bash
# Test product search agent
adk run retail-agents-team/product_search_agent/

# Test with specific input
adk run retail-agents-team/inventory_agent/ --replay input.json
```

### Check Agent Configuration
```bash
# Validate agent configuration
adk validate retail-agents-team/
```

### Monitor Agent Interactions
- Use ADK web interface for visual debugging
- Check agent logs for coordination patterns
- Monitor response times for each agent

## 📝 Best Practices

1. **Keep agents focused**: Each agent should have a clear, single purpose
2. **Document instructions**: Write clear, comprehensive instructions for each agent
3. **Use descriptive names**: Agent names should reflect their function
4. **Version control**: Track changes to individual agents
5. **Test independently**: Ensure each agent works standalone before integration

## 🔐 Security Considerations

- Never store sensitive data in agent instructions
- Use environment variables for API keys
- Implement proper authentication for production
- Sanitize user inputs before processing
- Follow data privacy regulations

## 📈 Performance Optimization

- Cache frequently accessed data
- Implement rate limiting for API calls
- Use parallel processing for independent tasks
- Monitor and optimize slow agents
- Consider agent-specific timeouts

## 🤝 Contributing

When contributing new agents:
1. Follow the modular structure
2. Write comprehensive instructions
3. Document the agent's purpose and capabilities
4. Add example queries
5. Test thoroughly before integration
