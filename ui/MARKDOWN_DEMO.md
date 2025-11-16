# Markdown Support Demo

This document contains examples of all supported Markdown features in the AI Retail Agent Team chatbot.

## How to Test

1. Start the server: `python ui/server.py`
2. Open http://127.0.0.1:8082
3. Copy and paste sections from this file into the chat
4. The agent's responses will render with full Markdown support!

---

## Supported Features

### Headings

# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6

### Text Formatting

**Bold text** and __also bold__

*Italic text* and _also italic_

***Bold and italic*** and ___also bold and italic___

~~Strikethrough text~~

### Lists

#### Unordered Lists

* Item 1
* Item 2
  * Nested item 2.1
  * Nested item 2.2
* Item 3

#### Ordered Lists

1. First item
2. Second item
   1. Nested item 2.1
   2. Nested item 2.2
3. Third item

#### Task Lists

- [x] Completed task
- [ ] Incomplete task
- [ ] Another incomplete task

### Links

[Visit Google](https://www.google.com)

[AI Retail Agent Team GitHub](https://github.com/Yash-Kavaiya/AI-Accelerate-Retail-Agent-Teams)

### Code

#### Inline Code

Use the `console.log()` function to print output.

The `markdown-body` class enables styling.

#### Code Blocks

```python
def search_products(query):
    """Search products using Elasticsearch"""
    results = es.search(
        index="products",
        query={"match": {"description": query}}
    )
    return results
```

```javascript
async function sendMessage(text) {
    const response = await fetch('/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
    });
    return response.json();
}
```

```json
{
  "product": "Wireless Headphones",
  "price": 99.99,
  "in_stock": true,
  "ratings": 4.5
}
```

### Blockquotes

> This is a blockquote.
> It can span multiple lines.
>
> And multiple paragraphs.

> **Note:** Blockquotes can contain other Markdown elements.

### Tables

| Agent | Primary Role | Tools | Response Time |
|-------|-------------|-------|---------------|
| Product Search | Product Discovery | 8 | < 500ms |
| Review Analysis | Review Intelligence | 6 | < 800ms |
| Inventory | Stock Management | 7 | < 300ms |
| Shopping | Transaction Processing | 7 | < 400ms |
| Customer Support | Service & Support | 5 | < 600ms |

#### Complex Table

| Feature | Description | Supported |
|---------|-------------|:---------:|
| **Headings** | H1 through H6 | ✅ |
| **Bold/Italic** | Text formatting | ✅ |
| **Lists** | Ordered & Unordered | ✅ |
| **Code Blocks** | Syntax highlighting | ✅ |
| **Tables** | Full table support | ✅ |
| **Links** | Hyperlinks | ✅ |
| **Images** | Image embedding | ✅ |
| **Blockquotes** | Quote styling | ✅ |

### Horizontal Rules

You can create horizontal rules with:

---

Three dashes, or:

***

Three asterisks, or:

___

Three underscores.

### Mixed Content Example

Here's a **comprehensive example** combining multiple Markdown features:

## Product Search Results

We found *5 products* matching your query. Here's a summary:

### Top Products

| Product | Price | Rating | In Stock |
|---------|-------|--------|----------|
| Sony WH-1000XM5 | $399.99 | ⭐⭐⭐⭐⭐ | ✅ Yes |
| Bose QuietComfort 45 | $329.99 | ⭐⭐⭐⭐ | ✅ Yes |
| AirPods Max | $549.99 | ⭐⭐⭐⭐⭐ | ❌ No |

### Customer Reviews Highlight

> "The **best noise cancellation** I've ever experienced. Highly recommended!"
> — Verified Buyer

#### Key Features

* Active Noise Cancellation
* 30-hour battery life
* Premium build quality
  * Aluminum construction
  * Soft ear cushions
* Multi-device connectivity

#### Technical Specifications

```yaml
Model: WH-1000XM5
Brand: Sony
Type: Over-ear
Wireless: Yes
Battery: 30 hours
Weight: 250g
Colors: [Black, Silver, Blue]
```

---

## Sample Agent Responses

### Product Recommendation

I found several **excellent options** for wireless headphones:

1. **Sony WH-1000XM5** ($399.99)
   - ⭐ Rating: 4.8/5
   - ✅ In stock
   - 🚚 Free 2-day shipping

2. **Bose QuietComfort 45** ($329.99)
   - ⭐ Rating: 4.6/5
   - ✅ In stock
   - 🎁 Includes carrying case

### Review Analysis

Based on `1,234 customer reviews`, here's the sentiment breakdown:

| Sentiment | Percentage | Count |
|-----------|-----------|-------|
| Positive 😊 | 78% | 963 |
| Neutral 😐 | 15% | 185 |
| Negative 😞 | 7% | 86 |

**Common themes:**
- ✅ Excellent sound quality
- ✅ Great battery life
- ❌ Expensive
- ❌ Heavy

### Code Example Response

Here's how to use our Python SDK:

```python
from retail_agent import ProductSearch

# Initialize the search agent
agent = ProductSearch(api_key="your_api_key")

# Search for products
results = agent.search(
    query="wireless headphones",
    filters={
        "price_max": 400,
        "rating_min": 4.0,
        "in_stock": True
    }
)

# Display results
for product in results:
    print(f"{product.name}: ${product.price}")
```

---

## Testing Checklist

Try asking the agent:

- [ ] "Show me a comparison table of laptops"
- [ ] "Explain how to search products with code examples"
- [ ] "What are the key features of product X?" (should get formatted lists)
- [ ] "Summarize customer reviews with sentiment analysis" (should get tables)
- [ ] "Give me technical specifications" (should get code blocks)

---

## Notes

- All agent responses automatically support Markdown
- User messages display as plain text
- Syntax highlighting works for 180+ programming languages
- Tables are fully responsive
- Code blocks include language detection

**Powered by:**
- [Marked.js](https://marked.js.org/) for Markdown parsing
- [Highlight.js](https://highlightjs.org/) for syntax highlighting
- [DOMPurify](https://github.com/cure53/DOMPurify) for XSS protection
