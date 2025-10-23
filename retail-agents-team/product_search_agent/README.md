# Product Search Agent - Elasticsearch Configuration

## Overview

The Product Search Agent is integrated with Elasticsearch for powerful, scalable product search capabilities. It supports fuzzy matching, advanced filtering, product comparison, and similarity search.

## Environment Variables

Configure the Elasticsearch connection using environment variables:

### Option 1: Elastic Cloud (Recommended for Production)
```bash
ELASTICSEARCH_CLOUD_ID=your_cloud_id_here
ELASTICSEARCH_API_KEY=your_api_key_here
```

### Option 2: Self-Hosted with API Key
```bash
ELASTICSEARCH_URL=https://your-elasticsearch-host:9200
ELASTICSEARCH_API_KEY=your_api_key_here
```

### Option 3: Self-Hosted with Basic Auth
```bash
ELASTICSEARCH_URL=https://your-elasticsearch-host:9200
ELASTICSEARCH_USERNAME=your_username
ELASTICSEARCH_PASSWORD=your_password
```

### Option 4: Local Development (No Auth)
```bash
ELASTICSEARCH_URL=http://localhost:9200
```

## Required Python Package

Install the Elasticsearch Python client:

```bash
pip install elasticsearch
```

## Index Schema

The agent expects products to be indexed with the following structure:

```json
{
  "name": "Wireless Headphones XM5",
  "description": "Premium noise-cancelling wireless headphones...",
  "category": "electronics",
  "brand": "Sony",
  "price": 299.99,
  "currency": "USD",
  "tags": ["wireless", "bluetooth", "noise-cancelling", "premium"],
  "rating": 4.5,
  "review_count": 1247,
  "in_stock": true,
  "popularity": 95,
  "specifications": {
    "battery_life": "30 hours",
    "weight": "250g",
    "color": ["Black", "Silver", "Blue"]
  },
  "images": [
    "https://example.com/images/product-1.jpg"
  ]
}
```

## Index Creation

Create the products index with proper mappings:

```bash
PUT /products
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1,
    "analysis": {
      "analyzer": {
        "product_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "asciifolding", "synonym_filter"]
        }
      },
      "filter": {
        "synonym_filter": {
          "type": "synonym",
          "synonyms": [
            "laptop, notebook, computer",
            "phone, mobile, smartphone",
            "headphones, earphones, earbuds"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "name": {
        "type": "text",
        "analyzer": "product_analyzer",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      },
      "description": {
        "type": "text",
        "analyzer": "product_analyzer"
      },
      "category": {
        "type": "keyword"
      },
      "brand": {
        "type": "keyword"
      },
      "price": {
        "type": "float"
      },
      "tags": {
        "type": "keyword"
      },
      "rating": {
        "type": "float"
      },
      "review_count": {
        "type": "integer"
      },
      "in_stock": {
        "type": "boolean"
      },
      "popularity": {
        "type": "integer"
      }
    }
  }
}
```

## Available Functions

### 1. search_products()

Search for products using natural language queries.

**Parameters:**
- `query` (str): Search query
- `index` (str): Index name (default: "products")
- `size` (int): Number of results (default: 10)
- `filters` (dict): Optional filters

**Example:**
```python
results = search_products(
    query="wireless headphones",
    size=20,
    filters={
        "brand": "Sony",
        "price": {"gte": 100, "lte": 500}
    }
)
```

**Response:**
```json
{
  "total": 45,
  "products": [
    {
      "id": "prod-123",
      "score": 12.5,
      "name": "Sony WH-1000XM5",
      "price": 299.99,
      ...
    }
  ],
  "query": "wireless headphones",
  "filters_applied": {"brand": "Sony"}
}
```

### 2. search_products_by_category()

Search within a specific category with price filtering.

**Parameters:**
- `category` (str): Product category
- `index` (str): Index name (default: "products")
- `size` (int): Number of results (default: 20)
- `min_price` (float): Minimum price
- `max_price` (float): Maximum price

**Example:**
```python
results = search_products_by_category(
    category="Electronics",
    min_price=100,
    max_price=500,
    size=30
)
```

### 3. get_product_by_id()

Retrieve a specific product by ID.

**Parameters:**
- `product_id` (str): Product ID
- `index` (str): Index name (default: "products")

**Example:**
```python
product = get_product_by_id("PROD-12345")
```

### 4. compare_products()

Compare multiple products side by side.

**Parameters:**
- `product_ids` (list): List of product IDs
- `index` (str): Index name (default: "products")

**Example:**
```python
comparison = compare_products([
    "PROD-001",
    "PROD-002",
    "PROD-003"
])
```

### 5. search_similar_products()

Find products similar to a given product.

**Parameters:**
- `product_id` (str): Product ID
- `index` (str): Index name (default: "products")
- `size` (int): Number of results (default: 5)

**Example:**
```python
similar = search_similar_products(
    product_id="PROD-12345",
    size=10
)
```

## Query Features

### Fuzzy Matching
Automatically handles typos and variations:
- "wireles headpones" → finds "wireless headphones"
- "samsng" → finds "samsung"

### Multi-Field Search
Searches across multiple fields with boosting:
- Product name (3x boost)
- Description (2x boost)
- Category
- Brand
- Tags

### Advanced Filtering
Supports multiple filter types:
- **Exact match**: `{"brand": "Sony"}`
- **Range**: `{"price": {"gte": 100, "lte": 500}}`
- **Multiple filters**: Combine any number of filters

### Sorting
Results sorted by:
1. Relevance score
2. Popularity (descending)

## Sample Data

Load sample products for testing:

```bash
POST /products/_bulk
{"index":{"_id":"1"}}
{"name":"Sony WH-1000XM5","description":"Premium noise-cancelling wireless headphones","category":"electronics","brand":"Sony","price":299.99,"tags":["wireless","bluetooth","noise-cancelling"],"rating":4.8,"review_count":2547,"in_stock":true,"popularity":98}
{"index":{"_id":"2"}}
{"name":"Apple AirPods Pro","description":"Wireless earbuds with active noise cancellation","category":"electronics","brand":"Apple","price":249.99,"tags":["wireless","bluetooth","noise-cancelling","earbuds"],"rating":4.6,"review_count":8932,"in_stock":true,"popularity":99}
{"index":{"_id":"3"}}
{"name":"Samsung Galaxy Buds Pro","description":"Premium wireless earbuds","category":"electronics","brand":"Samsung","price":199.99,"tags":["wireless","bluetooth","earbuds"],"rating":4.4,"review_count":1234,"in_stock":true,"popularity":85}
```

## Testing the Integration

### 1. Test Connection
```python
from product_search_agent.agent import get_elasticsearch_client

client = get_elasticsearch_client()
if client:
    print("✅ Connected to Elasticsearch")
    print(client.info())
else:
    print("❌ Connection failed")
```

### 2. Test Search
```python
from product_search_agent.agent import search_products

results = search_products("wireless headphones", size=5)
print(f"Found {results['total']} products")
for product in results['products']:
    print(f"- {product['name']} (${product['price']})")
```

### 3. Test with Agent
```bash
adk run retail-agents-team/product_search_agent/
```

Then query:
```
Find wireless headphones under $200
```

## Error Handling

The agent handles various error scenarios:

1. **No Elasticsearch Configuration**
   - Returns helpful error message
   - Suggests configuration steps

2. **Connection Failure**
   - Logs error details
   - Returns user-friendly message

3. **Index Not Found**
   - Returns appropriate error
   - Suggests index creation

4. **Search Errors**
   - Logs full error for debugging
   - Returns sanitized error to user

## Performance Optimization

### 1. Index Settings
- Use appropriate shard count (2-5 for small-medium datasets)
- Configure replicas for high availability
- Enable refresh interval optimization

### 2. Query Optimization
- Limit result size appropriately
- Use filters instead of queries when possible
- Leverage caching for frequent searches

### 3. Connection Pooling
The Elasticsearch client automatically manages connection pooling.

## Troubleshooting

### Issue: "Connection refused"
**Solution**: Verify Elasticsearch is running and URL is correct
```bash
curl -X GET "localhost:9200"
```

### Issue: "Authentication failed"
**Solution**: Check credentials and API key
```bash
# Test with curl
curl -X GET "https://your-host:9200" \
  -H "Authorization: ApiKey YOUR_API_KEY"
```

### Issue: "Index not found"
**Solution**: Create the index
```bash
# Create index with sample data
curl -X PUT "localhost:9200/products"
```

### Issue: "No results found"
**Solution**: 
1. Check if data is indexed
2. Verify field mappings
3. Test with match_all query

## Security Best Practices

1. **Use API Keys**: Prefer API keys over basic auth
2. **Limit Permissions**: Grant minimum required permissions
3. **Use HTTPS**: Always use encrypted connections in production
4. **Rotate Credentials**: Regularly update API keys
5. **Environment Variables**: Never hardcode credentials

## Monitoring

Monitor search performance:
- Query response times
- Search success/failure rates
- Popular search terms
- Zero-result queries

Use Elasticsearch monitoring tools:
- Kibana for visualization
- Elasticsearch APIs for metrics
- Application logs for debugging

## Next Steps

1. **Index Your Products**: Load your product catalog
2. **Test Searches**: Verify search quality
3. **Tune Relevance**: Adjust field boosting and analyzers
4. **Monitor Performance**: Track query metrics
5. **Optimize**: Refine based on usage patterns
