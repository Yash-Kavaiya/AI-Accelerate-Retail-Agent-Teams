import os
import logging
from typing import Dict, List, Any, Optional
from elasticsearch import Elasticsearch
from google.adk.agents import Agent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# Elasticsearch Configuration and Connection
# ============================================================================

def get_elasticsearch_client() -> Optional[Elasticsearch]:
    """
    Create and return an Elasticsearch client instance.
    Uses environment variables for credentials.
    """
    try:
        es_url = os.getenv("ELASTICSEARCH_CLOUD_URL")
        api_key = os.getenv("ELASTICSEARCH_API_KEY")
        
        if not es_url or not api_key:
            logger.error("Missing Elasticsearch credentials in environment variables")
            return None
        
        logger.info(f"Connecting to Elasticsearch at {es_url[:50]}...")
        return Elasticsearch(es_url, api_key=api_key)
    except Exception as e:
        logger.error(f"Failed to connect to Elasticsearch: {str(e)}")
        return None

# ============================================================================
# Product Search Functions
# ============================================================================

def search_products_by_text(
    query: str,
    index: str = "imagebind-embeddings",
    size: int = 10,
    gender: Optional[str] = None,
    article_type: Optional[str] = None,
    base_colour: Optional[str] = None,
    season: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for products using text query on productDisplayName field.
    Supports filtering by gender, article type, color, and season.
    
    Args:
        query: Text search query
        index: Elasticsearch index name
        size: Number of results to return
        gender: Filter by gender (e.g., "Men", "Women", "Boys", "Girls", "Unisex")
        article_type: Filter by article type (e.g., "Tshirts", "Shoes", "Watches")
        base_colour: Filter by base color (e.g., "Black", "Blue", "White")
        season: Filter by season (e.g., "Summer", "Winter", "Fall", "Spring")
    
    Returns:
        Dictionary containing search results with product details
    """
    es = get_elasticsearch_client()
    if not es:
        return {
            "error": "Elasticsearch client not configured",
            "message": "Please check ELASTICSEARCH_CLOUD_URL and ELASTICSEARCH_API_KEY env vars"
        }
    
    try:
        # Build query
        search_body = {
            "query": {
                "bool": {
                    "must": [{
                        "match": {
                            "productDisplayName": {
                                "query": query,
                                "fuzziness": "AUTO"
                            }
                        }
                    }]
                }
            },
            "size": size
        }
        
        # Add filters
        filters = []
        if gender:
            filters.append({"term": {"gender": gender}})
        if article_type:
            filters.append({"term": {"articleType": article_type}})
        if base_colour:
            filters.append({"term": {"baseColour": base_colour}})
        if season:
            filters.append({"term": {"season": season}})
        
        if filters:
            search_body["query"]["bool"]["filter"] = filters
        
        # Execute search
        response = es.search(index=index, body=search_body)
        
        return {
            "total": response['hits']['total']['value'],
            "products": [
                {
                    "id": hit['_id'],
                    "score": hit['_score'],
                    "product_name": hit['_source'].get('productDisplayName'),
                    "article_type": hit['_source'].get('articleType'),
                    "gender": hit['_source'].get('gender'),
                    "base_colour": hit['_source'].get('baseColour'),
                    "season": hit['_source'].get('season'),
                    "master_category": hit['_source'].get('masterCategory'),
                    "sub_category": hit['_source'].get('subCategory'),
                    "usage": hit['_source'].get('usage'),
                    "year": hit['_source'].get('year'),
                    "image_url": hit['_source'].get('image_url'),
                    "filename": hit['_source'].get('filename')
                }
                for hit in response['hits']['hits']
            ],
            "query": query,
            "filters_applied": {
                "gender": gender,
                "article_type": article_type,
                "base_colour": base_colour,
                "season": season
            }
        }
    except Exception as e:
        logger.error(f"Text search error: {str(e)}")
        return {
            "error": "Search failed",
            "message": str(e),
            "query": query
        }


def search_products_by_image_similarity(
    query_text: str,
    model_id: str = "",
    index: str = "imagebind-embeddings",
    size: int = 10,
    num_candidates: int = 100
) -> Dict[str, Any]:
    """
    Search for visually similar products using kNN search on image embeddings.
    Uses text-to-image embedding model to find products matching the description.
    
    Args:
        query_text: Natural language description of the product to find
        model_id: Embedding model ID (empty string uses default)
        index: Elasticsearch index name
        size: Number of results to return
        num_candidates: Number of candidates for kNN search
    
    Returns:
        Dictionary containing similar products based on visual embeddings
    """
    es = get_elasticsearch_client()
    if not es:
        return {
            "error": "Elasticsearch client not configured",
            "message": "Please check ELASTICSEARCH_CLOUD_URL and ELASTICSEARCH_API_KEY env vars"
        }
    
    try:
        retriever_object = {
            "standard": {
                "query": {
                    "knn": {
                        "field": "image_embedding",
                        "num_candidates": num_candidates,
                        "query_vector_builder": {
                            "text_embedding": {
                                "model_id": model_id,
                                "model_text": query_text
                            }
                        }
                    }
                }
            }
        }
        
        response = es.search(
            index=index,
            retriever=retriever_object,
            size=size
        )
        
        return {
            "total": len(response['hits']['hits']),
            "query": query_text,
            "products": [
                {
                    "id": hit['_id'],
                    "score": hit['_score'],
                    "product_name": hit['_source'].get('productDisplayName'),
                    "article_type": hit['_source'].get('articleType'),
                    "gender": hit['_source'].get('gender'),
                    "base_colour": hit['_source'].get('baseColour'),
                    "season": hit['_source'].get('season'),
                    "master_category": hit['_source'].get('masterCategory'),
                    "sub_category": hit['_source'].get('subCategory'),
                    "usage": hit['_source'].get('usage'),
                    "year": hit['_source'].get('year'),
                    "image_url": hit['_source'].get('image_url'),
                    "filename": hit['_source'].get('filename')
                }
                for hit in response['hits']['hits']
            ]
        }
    except Exception as e:
        logger.error(f"Image similarity search error: {str(e)}")
        return {
            "error": "Image similarity search failed",
            "message": str(e),
            "query": query_text
        }

def search_products_by_category(
    master_category: Optional[str] = None,
    sub_category: Optional[str] = None,
    article_type: Optional[str] = None,
    index: str = "imagebind-embeddings",
    size: int = 20
) -> Dict[str, Any]:
    """
    Search for products by category hierarchy.
    
    Args:
        master_category: Master category (e.g., "Apparel", "Accessories", "Footwear")
        sub_category: Sub category (e.g., "Topwear", "Bottomwear", "Shoes")
        article_type: Specific article type (e.g., "Tshirts", "Jeans", "Watches")
        index: Elasticsearch index name
        size: Number of results to return
    
    Returns:
        Dictionary containing products in the specified category
    """
    es = get_elasticsearch_client()
    if not es:
        return {
            "error": "Elasticsearch client not configured",
            "message": "Please check ELASTICSEARCH_CLOUD_URL and ELASTICSEARCH_API_KEY env vars"
        }
    
    try:
        filters = []
        
        if master_category:
            filters.append({"term": {"masterCategory": master_category}})
        if sub_category:
            filters.append({"term": {"subCategory": sub_category}})
        if article_type:
            filters.append({"term": {"articleType": article_type}})
        
        if not filters:
            return {
                "error": "At least one category filter is required",
                "message": "Please specify master_category, sub_category, or article_type"
            }
        
        search_body = {
            "query": {
                "bool": {
                    "filter": filters
                }
            },
            "size": size
        }
        
        response = es.search(index=index, body=search_body)
        
        return {
            "total": response['hits']['total']['value'],
            "filters_applied": {
                "master_category": master_category,
                "sub_category": sub_category,
                "article_type": article_type
            },
            "products": [
                {
                    "id": hit['_id'],
                    "score": hit['_score'],
                    "product_name": hit['_source'].get('productDisplayName'),
                    "article_type": hit['_source'].get('articleType'),
                    "gender": hit['_source'].get('gender'),
                    "base_colour": hit['_source'].get('baseColour'),
                    "season": hit['_source'].get('season'),
                    "master_category": hit['_source'].get('masterCategory'),
                    "sub_category": hit['_source'].get('subCategory'),
                    "usage": hit['_source'].get('usage'),
                    "year": hit['_source'].get('year'),
                    "image_url": hit['_source'].get('image_url'),
                    "filename": hit['_source'].get('filename')
                }
                for hit in response['hits']['hits']
            ]
        }
    except Exception as e:
        logger.error(f"Category search error: {str(e)}")
        return {
            "error": "Category search failed",
            "message": str(e)
        }

def get_product_by_id(
    product_id: str,
    index: str = "imagebind-embeddings"
) -> Dict[str, Any]:
    """
    Retrieve a specific product by its ID.
    
    Args:
        product_id: Elasticsearch document ID
        index: Elasticsearch index name
    
    Returns:
        Dictionary containing complete product details
    """
    es = get_elasticsearch_client()
    if not es:
        return {"error": "Elasticsearch client not configured"}
    
    try:
        response = es.get(index=index, id=product_id)
        source = response['_source']
        
        return {
            "id": response['_id'],
            "product_name": source.get('productDisplayName'),
            "article_type": source.get('articleType'),
            "gender": source.get('gender'),
            "base_colour": source.get('baseColour'),
            "season": source.get('season'),
            "master_category": source.get('masterCategory'),
            "sub_category": source.get('subCategory'),
            "usage": source.get('usage'),
            "year": source.get('year'),
            "image_url": source.get('image_url'),
            "filename": source.get('filename')
        }
    except Exception as e:
        logger.error(f"Error retrieving product {product_id}: {str(e)}")
        return {
            "error": "Product not found",
            "message": str(e),
            "product_id": product_id
        }

def compare_products(
    product_ids: List[str],
    index: str = "imagebind-embeddings"
) -> Dict[str, Any]:
    """
    Compare multiple products side by side by their IDs.
    
    Args:
        product_ids: List of product IDs to compare
        index: Elasticsearch index name
    
    Returns:
        Dictionary containing comparison of all products
    """
    es = get_elasticsearch_client()
    if not es:
        return {"error": "Elasticsearch client not configured"}
    
    products = []
    errors = []
    
    for product_id in product_ids:
        try:
            response = es.get(index=index, id=product_id)
            source = response['_source']
            products.append({
                "id": response['_id'],
                "product_name": source.get('productDisplayName'),
                "article_type": source.get('articleType'),
                "gender": source.get('gender'),
                "base_colour": source.get('baseColour'),
                "season": source.get('season'),
                "master_category": source.get('masterCategory'),
                "sub_category": source.get('subCategory'),
                "usage": source.get('usage'),
                "year": source.get('year'),
                "image_url": source.get('image_url'),
                "filename": source.get('filename')
            })
        except Exception as e:
            logger.warning(f"Product {product_id} not found: {str(e)}")
            errors.append({"product_id": product_id, "error": str(e)})
    
    if not products:
        return {
            "error": "No valid products found for comparison",
            "errors": errors
        }
    
    # Extract comparison attributes
    comparison = {
        "product_count": len(products),
        "products": products,
        "comparison_summary": {
            "genders": list(set(p['gender'] for p in products if p.get('gender'))),
            "article_types": list(set(p['article_type'] for p in products if p.get('article_type'))),
            "base_colours": list(set(p['base_colour'] for p in products if p.get('base_colour'))),
            "seasons": list(set(p['season'] for p in products if p.get('season'))),
            "categories": list(set(p['master_category'] for p in products if p.get('master_category')))
        }
    }
    
    if errors:
        comparison["errors"] = errors
    
    return comparison

def search_similar_products(
    product_id: str,
    index: str = "imagebind-embeddings",
    size: int = 10
) -> Dict[str, Any]:
    """
    Find visually similar products using the image embedding of a given product.
    Uses kNN search on the dense_vector field to find products with similar visual features.
    
    Args:
        product_id: ID of the product to find similar items for
        index: Elasticsearch index name
        size: Number of similar products to return
    
    Returns:
        Dictionary containing visually similar products
    """
    es = get_elasticsearch_client()
    if not es:
        return {"error": "Elasticsearch client not configured"}
    
    try:
        # First, get the original product's embedding
        original_product = es.get(index=index, id=product_id)
        
        if 'image_embedding' not in original_product['_source']:
            return {
                "error": "Product does not have image embedding",
                "product_id": product_id
            }
        
        query_vector = original_product['_source']['image_embedding']
        
        # Search for similar products using kNN
        search_body = {
            "knn": {
                "field": "image_embedding",
                "query_vector": query_vector,
                "k": size + 1,  # +1 to exclude the original product
                "num_candidates": 100
            },
            "_source": {
                "excludes": ["image_embedding"]  # Exclude embedding from results
            }
        }
        
        response = es.search(index=index, body=search_body)
        
        # Filter out the original product from results
        similar_products = []
        for hit in response['hits']['hits']:
            if hit['_id'] != product_id:
                source = hit['_source']
                similar_products.append({
                    "id": hit['_id'],
                    "score": hit['_score'],
                    "product_name": source.get('productDisplayName'),
                    "article_type": source.get('articleType'),
                    "gender": source.get('gender'),
                    "base_colour": source.get('baseColour'),
                    "season": source.get('season'),
                    "master_category": source.get('masterCategory'),
                    "sub_category": source.get('subCategory'),
                    "usage": source.get('usage'),
                    "year": source.get('year'),
                    "image_url": source.get('image_url'),
                    "filename": source.get('filename')
                })
        
        return {
            "original_product_id": product_id,
            "original_product_name": original_product['_source'].get('productDisplayName'),
            "similar_products": similar_products[:size],
            "count": len(similar_products[:size])
        }
    except Exception as e:
        logger.error(f"Similar products search error: {str(e)}")
        return {
            "error": "Similar products search failed",
            "message": str(e),
            "product_id": product_id
        }


def get_available_filters(
    index: str = "imagebind-embeddings"
) -> Dict[str, Any]:
    """
    Get all available filter options from the index.
    Returns unique values for gender, article types, colors, seasons, etc.
    
    Args:
        index: Elasticsearch index name
    
    Returns:
        Dictionary containing all available filter values
    """
    es = get_elasticsearch_client()
    if not es:
        return {"error": "Elasticsearch client not configured"}
    
    try:
        search_body = {
            "size": 0,
            "aggs": {
                "genders": {
                    "terms": {"field": "gender", "size": 50}
                },
                "article_types": {
                    "terms": {"field": "articleType", "size": 100}
                },
                "base_colours": {
                    "terms": {"field": "baseColour", "size": 100}
                },
                "seasons": {
                    "terms": {"field": "season", "size": 20}
                },
                "master_categories": {
                    "terms": {"field": "masterCategory", "size": 50}
                },
                "sub_categories": {
                    "terms": {"field": "subCategory", "size": 100}
                },
                "usage": {
                    "terms": {"field": "usage", "size": 50}
                }
            }
        }
        
        response = es.search(index=index, body=search_body)
        aggs = response['aggregations']
        
        return {
            "total_products": response['hits']['total']['value'],
            "available_filters": {
                "genders": [bucket['key'] for bucket in aggs['genders']['buckets']],
                "article_types": [bucket['key'] for bucket in aggs['article_types']['buckets']],
                "base_colours": [bucket['key'] for bucket in aggs['base_colours']['buckets']],
                "seasons": [bucket['key'] for bucket in aggs['seasons']['buckets']],
                "master_categories": [bucket['key'] for bucket in aggs['master_categories']['buckets']],
                "sub_categories": [bucket['key'] for bucket in aggs['sub_categories']['buckets']],
                "usage": [bucket['key'] for bucket in aggs['usage']['buckets']]
            }
        }
    except Exception as e:
        logger.error(f"Error fetching available filters: {str(e)}")
        return {
            "error": "Failed to fetch available filters",
            "message": str(e)
        }

# ============================================================================
# Define the Agent with Tools
# ============================================================================

root_agent = Agent(
    name='product_search_agent',
    model='gemini-2.0-flash',
    description='Specialized agent for searching fashion products using visual embeddings and text search in Elasticsearch.',
    instruction="""
    You are a fashion product search specialist with access to a powerful Elasticsearch database 
    containing fashion items with visual embeddings (ImageBind). Your role is to:

    1. **Text-based Product Search**:
       - Use search_products_by_text() for searching by product name/description
       - Apply filters: gender (Men/Women/Boys/Girls/Unisex), article type, color, season
       - Handle variations and fuzzy matching for typos
       - Example: "Find blue t-shirts for men"

    2. **Visual Similarity Search**:
       - Use search_products_by_image_similarity() for finding products matching a description
       - Leverages ImageBind embeddings (1024-dimensional dense vectors)
       - Great for: "Show me products that look like a casual summer dress"
       - Uses kNN search with cosine similarity

    3. **Category Browsing**:
       - Use search_products_by_category() to browse by hierarchy
       - Master categories: Apparel, Accessories, Footwear, Personal Care, etc.
       - Sub categories: Topwear, Bottomwear, Shoes, Watches, etc.
       - Article types: Tshirts, Jeans, Casual Shoes, Watches, etc.

    4. **Product Details**:
       - Use get_product_by_id() for complete product information
       - Includes: name, type, gender, color, season, category, year, image URL
       - Display image_url for visual reference

    5. **Product Comparison**:
       - Use compare_products() for side-by-side comparison
       - Highlights: color differences, seasonal availability, usage patterns
       - Compare features across multiple products

    6. **Similar Products**:
       - Use search_similar_products() to find visually similar items
       - Based on image embeddings (visual features)
       - Great for recommendations: "More items like this"

    7. **Available Filters**:
       - Use get_available_filters() to show all browsable options
       - Helps users discover: all genders, colors, types, seasons available

    **Available Functions**:
    - search_products_by_text(query, gender, article_type, base_colour, season, size)
    - search_products_by_image_similarity(query_text, model_id, size, num_candidates)
    - search_products_by_category(master_category, sub_category, article_type, size)
    - get_product_by_id(product_id)
    - compare_products(product_ids)
    - search_similar_products(product_id, size)
    - get_available_filters()

    **Fashion Product Schema**:
    - productDisplayName: Full product name
    - articleType: Specific product type (e.g., Tshirts, Jeans)
    - gender: Target gender (Men, Women, Boys, Girls, Unisex)
    - baseColour: Primary color
    - season: Seasonal category (Summer, Winter, Fall, Spring)
    - masterCategory: Top-level category (Apparel, Accessories, Footwear)
    - subCategory: Secondary category (Topwear, Bottomwear, Shoes)
    - usage: Usage context (Casual, Formal, Sports, Ethnic, Party)
    - year: Product year
    - image_url: Product image URL
    - image_embedding: 1024-dim visual features (ImageBind)

    **Best Practices**:
    - Always show image_url when available for visual reference
    - Use image similarity search for "looks like" or visual queries
    - Use text search for specific product names or descriptions
    - Combine filters for precise results (gender + color + type)
    - Suggest similar products for recommendations
    - Use get_available_filters() when users ask "what options do you have?"

    Present results in a clear, organized manner with images and key attributes highlighted.
    Be helpful in guiding customers to find their perfect fashion items!
    """,
    tools=[
        search_products_by_text,
        search_products_by_image_similarity,
        search_products_by_category,
        get_product_by_id,
        compare_products,
        search_similar_products,
        get_available_filters
    ]
)

