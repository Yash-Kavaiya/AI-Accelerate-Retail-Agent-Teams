import os
import logging
from typing import Dict, List, Any, Optional
from elasticsearch import Elasticsearch
from google.adk.agents import Agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# Elasticsearch Configuration and Connection
# ============================================================================

def get_elasticsearch_client() -> Optional[Elasticsearch]:
    """
    Create and return an Elasticsearch client instance from env/config.
    Supports Elastic Cloud, API Key, user/pass, or local mode.
    """
    try:
        # These should be set via environment variables for production!
        cloud_id = os.getenv("ELASTICSEARCH_CLOUD_ID", "")
        api_key = os.getenv("ELASTICSEARCH_API_KEY", "")
        es_url = os.getenv('ELASTICSEARCH_URL', 'http://localhost:9200')
        username = os.getenv('ELASTICSEARCH_USERNAME', "")
        password = os.getenv('ELASTICSEARCH_PASSWORD', "")

        # Cloud mode (Elastic Cloud)
        if cloud_id and api_key:
            logger.info("Connecting to Elasticsearch Cloud...")
            return Elasticsearch(cloud_id=cloud_id, api_key=api_key)
        # API-key/URL mode
        if es_url and api_key:
            logger.info(f"Connecting to Elasticsearch at {es_url} with API key...")
            return Elasticsearch(es_url, api_key=api_key)
        # Username/password
        if es_url and username and password:
            logger.info(f"Connecting to Elasticsearch at {es_url} with basic auth...")
            return Elasticsearch(es_url, basic_auth=(username, password))
        # Local fallback
        logger.info(f"Connecting to Elasticsearch at {es_url} without authentication...")
        return Elasticsearch(es_url)
    except Exception as e:
        logger.error(f"Failed to connect to Elasticsearch: {str(e)}")
        return None

# ============================================================================
# Product Search Functions
# ============================================================================

def search_products(query: str,
                   index: str = "products",
                   size: int = 10,
                   filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Search for products in Elasticsearch using a text query and optional filters.
    """
    es = get_elasticsearch_client()
    if not es:
        return {
            "error": "Elasticsearch client not configured",
            "message": "Please check ELASTICSEARCH_URL/ELASTICSEARCH_CLOUD_ID env vars"
        }
    try:
        # Base query config
        search_body = {
            "query": {
                "bool": {
                    "must": [{
                        "multi_match": {
                            "query": query,
                            "fields": [
                                "name^3", "description^2", "category", "brand", "tags"
                            ],
                            "type": "best_fields",
                            "fuzziness": "AUTO"
                        }
                    }]
                }
            },
            "size": size,
            "sort": [
                "_score",
                {"popularity": {"order": "desc"}}
            ]
        }
        # Add filters
        if filters:
            filter_clauses = []
            for field, value in filters.items():
                if isinstance(value, dict):
                    filter_clauses.append({"range": {field: value}})
                else:
                    filter_clauses.append({"term": {field: value}})
            if filter_clauses:
                search_body["query"]["bool"]["filter"] = filter_clauses
        # Search
        response = es.search(index=index, body=search_body)
        return {
            "total": response['hits']['total']['value'],
            "products": [
                {
                    "id": hit['_id'],
                    "score": hit['_score'],
                    **hit['_source']
                }
                for hit in response['hits']['hits']
            ],
            "query": query,
            "filters_applied": filters or {}
        }
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return {
            "error": "Search failed",
            "message": str(e),
            "query": query
        }

def search_products_by_category(category: str,
                               index: str = "products",
                               size: int = 20,
                               min_price: Optional[float] = None,
                               max_price: Optional[float] = None) -> Dict[str, Any]:
    """
    Search for products within a specific category and price range.
    """
    filters = {"category": category.lower()}
    if min_price is not None or max_price is not None:
        price_filter = {}
        if min_price is not None:
            price_filter["gte"] = min_price
        if max_price is not None:
            price_filter["lte"] = max_price
        filters["price"] = price_filter
    return search_products("*", index=index, size=size, filters=filters)

def get_product_by_id(product_id: str,
                     index: str = "products") -> Dict[str, Any]:
    """
    Retrieve a specific product by its ID.
    """
    es = get_elasticsearch_client()
    if not es:
        return {"error": "Elasticsearch client not configured"}
    try:
        response = es.get(index=index, id=product_id)
        return {"id": response['_id'], **response['_source']}
    except Exception as e:
        logger.error(f"Error retrieving product {product_id}: {str(e)}")
        return {
            "error": "Product not found",
            "message": str(e),
            "product_id": product_id
        }

def compare_products(product_ids: List[str],
                     index: str = "products") -> Dict[str, Any]:
    """
    Compare multiple products side by side by their IDs.
    """
    es = get_elasticsearch_client()
    if not es:
        return {"error": "Elasticsearch client not configured"}
    products = []
    for product_id in product_ids:
        try:
            response = es.get(index=index, id=product_id)
            products.append({"id": response['_id'], **response['_source']})
        except Exception as e:
            logger.warning(f"Product {product_id} not found: {str(e)}")
    if not products:
        return {"error": "No valid products found for comparison"}
    comparison_fields = set()
    for product in products:
        comparison_fields.update(product.keys())
    return {
        "products": products,
        "comparison_fields": sorted(list(comparison_fields)),
        "product_count": len(products)
    }

def search_similar_products(product_id: str,
                            index: str = "products",
                            size: int = 5) -> Dict[str, Any]:
    """
    Return products similar to the given product (more-like-this query).
    """
    es = get_elasticsearch_client()
    if not es:
        return {"error": "Elasticsearch client not configured"}
    try:
        search_body = {
            "query": {
                "more_like_this": {
                    "fields": ["name", "description", "category", "tags"],
                    "like": [{"_index": index, "_id": product_id}],
                    "min_term_freq": 1,
                    "min_doc_freq": 1,
                    "max_query_terms": 12
                }
            },
            "size": size
        }
        response = es.search(index=index, body=search_body)
        return {
            "original_product_id": product_id,
            "similar_products": [
                {
                    "id": hit['_id'],
                    "score": hit['_score'],
                    **hit['_source']
                }
                for hit in response['hits']['hits']
            ],
            "count": len(response['hits']['hits'])
        }
    except Exception as e:
        logger.error(f"Similar products search error: {str(e)}")
        return {
            "error": "Similar products search failed",
            "message": str(e),
            "product_id": product_id
        }

# ============================================================================
# Define the Agent with Tools
# ============================================================================

root_agent = Agent(
    name='product_search_agent',
    model='gemini-2.0-flash',
    description='Specialized agent for searching and finding products in the retail inventory using Elasticsearch.',
    instruction="""
    You are a product search specialist with access to a powerful Elasticsearch-powered 
    product database. Your role is to:

    1. Search for products based on customer queries:
       - Use the search_products() function for general text searches
       - Use search_products_by_category() for category-specific searches
       - Apply filters for price ranges, brands, and other attributes
       - Handle fuzzy matching for typos and variations
    2. Provide detailed product information:
       - Use get_product_by_id() to retrieve specific product details
       - Present complete product specifications
       - Show pricing information and available discounts
       - Include product availability status
       - Display product images and descriptions
    3. Compare products:
       - Use compare_products() to create side-by-side comparisons
       - Highlight key differences and similarities
       - Compare features, prices, and ratings
       - Recommend best value options based on customer needs
    4. Suggest alternatives:
       - Use search_similar_products() to find similar items
       - Recommend products when items are unavailable
       - Suggest upgraded or downgraded options based on budget
       - Provide cross-sell and upsell recommendations
    5. Advanced filtering:
       - Filter by customer ratings and reviews
       - Filter by popularity and best sellers
       - Filter by price ranges
       - Apply multiple filters simultaneously
       - Sort results by relevance, price, or popularity

    Available Functions:
    - search_products(query, size, filters): General product search
    - search_products_by_category(category, min_price, max_price): Category-based search
    - get_product_by_id(product_id): Get specific product details
    - compare_products(product_ids): Compare multiple products
    - search_similar_products(product_id, size): Find similar products

    Always provide accurate, up-to-date product information and be helpful in guiding 
    customers to find the perfect products for their needs. Present information in a 
    clear, organized manner with relevant details highlighted.

    When Elasticsearch is not configured, inform users about the setup requirements
    and provide mock data for demonstration purposes.
    """,
    tools=[
        search_products,
        search_products_by_category,
        get_product_by_id,
        compare_products,
        search_similar_products
    ]
)

