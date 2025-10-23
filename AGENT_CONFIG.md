# Agent Configuration Details

This document provides detailed configuration information for each agent in the retail system.

## Agent Configuration Parameters

Each agent uses the following standard parameters:

- **name**: Unique identifier for the agent
- **model**: The LLM model used (e.g., `gemini-2.0-flash`)
- **description**: Short summary of agent's purpose
- **instruction**: Detailed behavior guidelines and responsibilities
- **tools**: External tools available to the agent (optional)
- **sub_agents**: List of child agents (only for coordinator)

## Root Coordinator Agent

```yaml
Name: retail_coordinator
Model: gemini-2.0-flash
Type: Coordinator
Sub-agents: 5
```

**Responsibilities**:
- Request routing and orchestration
- Multi-agent coordination
- Context management
- Response synthesis

**Decision Logic**:
- Analyzes customer intent
- Routes to single or multiple agents
- Manages agent dependencies
- Combines responses intelligently

## Product Search Agent

```yaml
Name: product_search_agent
Model: gemini-2.0-flash
Type: Specialized
Domain: Product Discovery
```

**Core Capabilities**:
1. Product Search
2. Advanced Filtering
3. Product Comparison
4. Alternative Suggestions
5. Detailed Information Retrieval

**Typical Response Format**:
```json
{
  "products": [...],
  "filters_applied": {...},
  "total_results": 123,
  "recommendations": [...]
}
```

## Review Text Analysis Agent

```yaml
Name: review_text_analysis_agent
Model: gemini-2.0-flash
Type: Specialized
Domain: Text Analytics
```

**Analysis Types**:
1. Sentiment Analysis (positive/negative/neutral)
2. Theme Extraction
3. Product Insights
4. Review Quality Assessment
5. Statistical Analysis

**Typical Response Format**:
```json
{
  "sentiment": {
    "overall": "positive",
    "score": 0.85,
    "distribution": {...}
  },
  "themes": [...],
  "insights": {...}
}
```

## Inventory Agent

```yaml
Name: inventory_agent
Model: gemini-2.0-flash
Type: Specialized
Domain: Inventory Management
```

**Tracking Capabilities**:
1. Real-time Stock Levels
2. Multi-location Tracking
3. Availability Status
4. Delivery Estimation
5. Reservation Management

**Typical Response Format**:
```json
{
  "product_id": "ABC123",
  "availability": "in_stock",
  "quantity": 45,
  "locations": [...],
  "estimated_delivery": "2-3 days"
}
```

## Shopping Agent

```yaml
Name: shopping_agent
Model: gemini-2.0-flash
Type: Specialized
Domain: E-commerce Transactions
```

**Transaction Capabilities**:
1. Cart Management
2. Price Calculation
3. Discount Application
4. Checkout Processing
5. Order Confirmation

**Typical Response Format**:
```json
{
  "cart": {
    "items": [...],
    "subtotal": 299.99,
    "tax": 24.00,
    "shipping": 9.99,
    "discount": -30.00,
    "total": 303.98
  }
}
```

## Customer Support Agent

```yaml
Name: customer_support_agent
Model: gemini-2.0-flash
Type: Specialized
Domain: Customer Service
```

**Support Capabilities**:
1. Order Inquiries
2. Returns/Refunds
3. Issue Resolution
4. Policy Information
5. Escalation Management

**Typical Response Format**:
```json
{
  "order_id": "ORD-12345",
  "status": "shipped",
  "tracking": "1Z999AA10123456784",
  "support_action": "return_initiated",
  "resolution": {...}
}
```

## Agent Communication Protocol

### Request Format to Sub-agents

```json
{
  "agent": "product_search_agent",
  "query": "Find wireless headphones under $100",
  "context": {
    "user_preferences": {...},
    "conversation_history": [...]
  }
}
```

### Response Format from Sub-agents

```json
{
  "agent": "product_search_agent",
  "status": "success",
  "data": {...},
  "metadata": {
    "processing_time": "0.5s",
    "confidence": 0.95
  }
}
```

## Performance Metrics

### Target Metrics

| Agent | Response Time | Success Rate | Handoff Rate |
|-------|---------------|--------------|--------------|
| Coordinator | < 0.2s | > 98% | N/A |
| Product Search | < 1.0s | > 95% | < 5% |
| Review Analysis | < 2.0s | > 90% | < 10% |
| Inventory | < 0.5s | > 99% | < 2% |
| Shopping | < 1.0s | > 98% | < 5% |
| Customer Support | < 1.5s | > 95% | < 15% |

## Configuration Best Practices

### Instruction Design

1. **Be Specific**: Clear, detailed instructions
2. **Use Examples**: Include sample scenarios
3. **Define Boundaries**: Specify what agent should/shouldn't do
4. **Error Handling**: Describe fallback behaviors
5. **Tone Guidelines**: Set communication style

### Model Selection

- **gemini-2.0-flash**: Fast responses, good for most tasks
- **gemini-2.0-pro**: Complex reasoning, advanced analysis
- **gemini-1.5-flash**: Cost-effective option

### Optimization Tips

1. **Cache Common Queries**: Store frequent request results
2. **Parallel Processing**: Use when agents are independent
3. **Timeout Configuration**: Set appropriate timeouts per agent
4. **Rate Limiting**: Implement per-agent rate limits
5. **Monitoring**: Track agent performance metrics

## Environment Variables

```bash
# Required
GOOGLE_API_KEY=your_api_key_here

# Optional
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_REGION=us-central1

# Agent-specific (if needed)
PRODUCT_SEARCH_CACHE_TTL=3600
INVENTORY_REFRESH_RATE=60
SHOPPING_CART_TIMEOUT=1800
```

## Agent Extensions

### Future Tool Additions

Each agent can be extended with specialized tools:

**Product Search Agent**:
- `search_database_tool`
- `compare_products_tool`
- `recommendation_engine_tool`

**Review Analysis Agent**:
- `sentiment_analysis_tool`
- `nlp_processing_tool`
- `review_aggregator_tool`

**Inventory Agent**:
- `inventory_query_tool`
- `warehouse_api_tool`
- `shipping_calculator_tool`

**Shopping Agent**:
- `payment_processor_tool`
- `tax_calculator_tool`
- `coupon_validator_tool`

**Customer Support Agent**:
- `order_lookup_tool`
- `refund_processor_tool`
- `ticket_system_tool`

## Testing Configuration

### Unit Tests per Agent

```python
# Example test for product_search_agent
def test_product_search():
    query = "wireless headphones under $100"
    result = product_search_agent.process(query)
    assert result.status == "success"
    assert len(result.products) > 0
    assert all(p.price < 100 for p in result.products)
```

### Integration Tests

```python
# Example test for multi-agent workflow
def test_product_purchase_flow():
    # Search product
    products = coordinator.route("Find iPhone 15")
    
    # Check inventory
    availability = coordinator.route("Check stock for iPhone 15")
    
    # Add to cart
    cart = coordinator.route("Add iPhone 15 to cart")
    
    assert cart.items[0].product == "iPhone 15"
```

## Monitoring and Logging

### Log Levels per Agent

- **DEBUG**: Detailed execution information
- **INFO**: General operational messages
- **WARNING**: Non-critical issues
- **ERROR**: Error conditions
- **CRITICAL**: System failures

### Metrics to Monitor

1. Request count per agent
2. Average response time
3. Error rates
4. Agent handoff frequency
5. Customer satisfaction scores

## Version Management

Track agent configurations with version numbers:

```python
AGENT_VERSION = "1.0.0"  # Major.Minor.Patch

# Update when:
# Major: Breaking changes to agent behavior
# Minor: New features or capabilities
# Patch: Bug fixes or minor improvements
```
