# Product Search Agent - Quick Reference

## 🚀 Quick Start (5 Minutes)

### 1. Install
```bash
pip install elasticsearch
```

### 2. Configure (choose one)
```bash
# Local Elasticsearch
export ELASTICSEARCH_URL=http://localhost:9200

# OR Elastic Cloud
export ELASTICSEARCH_CLOUD_ID=your_cloud_id
export ELASTICSEARCH_API_KEY=your_api_key
```

### 3. Run
```bash
adk run retail-agents-team/product_search_agent/
```

## 📝 Function Cheat Sheet

### Search Products
```python
search_products(
    query="wireless headphones",
    size=10,
    filters={"brand": "Sony", "price": {"lte": 300}}
)
```

### Search by Category
```python
search_products_by_category(
    category="Electronics",
    min_price=100,
    max_price=500
)
```

### Get Product
```python
get_product_by_id("PROD-12345")
```

### Compare Products
```python
compare_products(["PROD-001", "PROD-002", "PROD-003"])
```

### Similar Products
```python
search_similar_products("PROD-12345", size=5)
```

## 🎯 Common Queries

| User Query | Function Used | Filters |
|-----------|---------------|---------|
| "Find wireless headphones" | `search_products()` | None |
| "Sony headphones under $300" | `search_products()` | `brand`, `price` |
| "Show Electronics category" | `search_products_by_category()` | `category` |
| "Products like PROD-123" | `search_similar_products()` | None |
| "Compare these 3 products" | `compare_products()` | None |

## ⚙️ Configuration Options

| Environment Variable | Example | Description |
|---------------------|---------|-------------|
| `ELASTICSEARCH_URL` | `http://localhost:9200` | Elasticsearch endpoint |
| `ELASTICSEARCH_CLOUD_ID` | `my-deployment:dXMt...` | Elastic Cloud ID |
| `ELASTICSEARCH_API_KEY` | `VnVhQ2ZHY0JDZGJr...` | API key for auth |
| `ELASTICSEARCH_USERNAME` | `elastic` | Username (basic auth) |
| `ELASTICSEARCH_PASSWORD` | `changeme` | Password (basic auth) |

## 🔍 Filter Examples

### Exact Match
```python
filters={"brand": "Sony"}
```

### Price Range
```python
filters={"price": {"gte": 100, "lte": 500}}
```

### Multiple Filters
```python
filters={
    "brand": "Sony",
    "category": "electronics",
    "price": {"lte": 300},
    "in_stock": True
}
```

## 📊 Response Format

```json
{
  "total": 45,
  "products": [
    {
      "id": "prod-123",
      "score": 12.5,
      "name": "Product Name",
      "price": 299.99,
      "brand": "Sony",
      "category": "electronics"
    }
  ],
  "query": "wireless headphones",
  "filters_applied": {"brand": "Sony"}
}
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Connection refused" | Start Elasticsearch: `docker run -p 9200:9200 elasticsearch:8.11.0` |
| "Import error" | Install: `pip install elasticsearch` |
| "Index not found" | Create index: `curl -X PUT localhost:9200/products` |
| "No results" | Check data: `curl localhost:9200/products/_search` |
| "Auth failed" | Verify credentials in `.env` |

## 📖 Documentation

- **Full Guide**: `README.md` - Complete setup and usage
- **Implementation**: `IMPLEMENTATION.md` - Technical details
- **Code**: `agent.py` - Source code with comments

## 💡 Pro Tips

1. **Fuzzy matching**: Typos are automatically handled
2. **Field boosting**: Product names have 3x weight
3. **Combine filters**: Use multiple filters for precise results
4. **Similar products**: Great for recommendations
5. **Comparison**: Perfect for "vs" queries

## 🎯 Test Commands

```bash
# Test connection
curl http://localhost:9200

# Create index
curl -X PUT localhost:9200/products

# Check data
curl localhost:9200/products/_count

# Test search
curl -X POST localhost:9200/products/_search -H 'Content-Type: application/json' -d'
{
  "query": {"match": {"name": "headphones"}}
}'

# Test agent
adk run retail-agents-team/product_search_agent/
```

## 📞 Need Help?

1. Check `README.md` for detailed documentation
2. Review `IMPLEMENTATION.md` for technical details
3. Check Elasticsearch logs: `docker logs <container-id>`
4. Enable debug logging in `agent.py`

---

**Ready to search! 🚀**
