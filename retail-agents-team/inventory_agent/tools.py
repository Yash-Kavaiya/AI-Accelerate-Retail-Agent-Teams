"""
Inventory Agent Tools
Functions for managing and querying retail store inventory using Elasticsearch.
"""

import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from elasticsearch import Elasticsearch
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
    
    Returns:
        Elasticsearch: Connected Elasticsearch client or None on failure
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
# Inventory Query Functions
# ============================================================================

def check_product_inventory(
    product_id: str,
    store_id: Optional[str] = None,
    region: Optional[str] = None,
    index: str = "retail_store_inventory"
) -> Dict[str, Any]:
    """
    Check real-time inventory levels for a specific product.
    Can filter by store ID or region for location-specific availability.
    
    Args:
        product_id: Product ID to check inventory for
        store_id: Optional store ID to check specific location
        region: Optional region filter (e.g., "North", "South", "East", "West")
        index: Elasticsearch index name
    
    Returns:
        Dictionary containing inventory levels, stock status, and location details
    """
    es = get_elasticsearch_client()
    if not es:
        return {
            "error": "Elasticsearch client not configured",
            "message": "Please check ELASTICSEARCH_CLOUD_URL and ELASTICSEARCH_API_KEY"
        }
    
    try:
        # Build query filters
        filters = [{"term": {"Product ID": product_id}}]
        
        if store_id:
            filters.append({"term": {"Store ID": store_id}})
        if region:
            filters.append({"term": {"Region": region}})
        
        retriever_object = {
            "standard": {
                "query": {
                    "bool": {
                        "filter": filters
                    }
                }
            }
        }
        
        response = es.search(
            index=index,
            retriever=retriever_object,
            size=100
        )
        
        hits = response['hits']['hits']
        
        if not hits:
            return {
                "product_id": product_id,
                "store_id": store_id,
                "region": region,
                "status": "not_found",
                "message": "No inventory records found for this product"
            }
        
        # Aggregate inventory data
        total_inventory = 0
        locations = []
        
        for hit in hits:
            source = hit['_source']
            inventory_level = source.get('Inventory Level', 0)
            total_inventory += inventory_level
            
            locations.append({
                "store_id": source.get('Store ID'),
                "region": source.get('Region'),
                "inventory_level": inventory_level,
                "units_sold": source.get('Units Sold', 0),
                "units_ordered": source.get('Units Ordered', 0),
                "price": source.get('Price', 0),
                "discount": source.get('Discount', 0),
                "date": source.get('Date'),
                "category": source.get('Category')
            })
        
        # Determine stock status
        if total_inventory == 0:
            stock_status = "out_of_stock"
        elif total_inventory < 10:
            stock_status = "low_stock"
        elif total_inventory < 50:
            stock_status = "moderate_stock"
        else:
            stock_status = "in_stock"
        
        return {
            "product_id": product_id,
            "total_inventory": total_inventory,
            "stock_status": stock_status,
            "location_count": len(locations),
            "locations": locations,
            "filters_applied": {
                "store_id": store_id,
                "region": region
            }
        }
        
    except Exception as e:
        logger.error(f"Error checking product inventory: {str(e)}")
        return {
            "error": "Inventory check failed",
            "message": str(e),
            "product_id": product_id
        }


def search_inventory_by_category(
    category: str,
    region: Optional[str] = None,
    min_inventory: Optional[int] = None,
    max_inventory: Optional[int] = None,
    index: str = "retail_store_inventory",
    size: int = 50
) -> Dict[str, Any]:
    """
    Search inventory by product category with optional filters.
    
    Args:
        category: Product category to search for
        region: Optional region filter
        min_inventory: Minimum inventory level filter
        max_inventory: Maximum inventory level filter
        index: Elasticsearch index name
        size: Maximum number of results to return
    
    Returns:
        Dictionary containing matching inventory records
    """
    es = get_elasticsearch_client()
    if not es:
        return {"error": "Elasticsearch client not configured"}
    
    try:
        # Build query with multi_match for category search
        query_must = [{
            "multi_match": {
                "query": category,
                "fields": ["Category"]
            }
        }]
        
        filters = []
        if region:
            filters.append({"term": {"Region": region}})
        
        # Add inventory range filters
        if min_inventory is not None or max_inventory is not None:
            range_filter = {"range": {"Inventory Level": {}}}
            if min_inventory is not None:
                range_filter["range"]["Inventory Level"]["gte"] = min_inventory
            if max_inventory is not None:
                range_filter["range"]["Inventory Level"]["lte"] = max_inventory
            filters.append(range_filter)
        
        retriever_object = {
            "standard": {
                "query": {
                    "bool": {
                        "must": query_must,
                        "filter": filters
                    }
                }
            }
        }
        
        response = es.search(
            index=index,
            retriever=retriever_object,
            size=size
        )
        
        products = []
        total_inventory = 0
        
        for hit in response['hits']['hits']:
            source = hit['_source']
            inventory = source.get('Inventory Level', 0)
            total_inventory += inventory
            
            products.append({
                "product_id": source.get('Product ID'),
                "store_id": source.get('Store ID'),
                "category": source.get('Category'),
                "region": source.get('Region'),
                "inventory_level": inventory,
                "units_sold": source.get('Units Sold', 0),
                "units_ordered": source.get('Units Ordered', 0),
                "price": source.get('Price', 0),
                "discount": source.get('Discount', 0),
                "demand_forecast": source.get('Demand Forecast', 0),
                "date": source.get('Date')
            })
        
        return {
            "category": category,
            "total_results": response['hits']['total']['value'],
            "total_inventory": total_inventory,
            "products": products,
            "filters_applied": {
                "region": region,
                "min_inventory": min_inventory,
                "max_inventory": max_inventory
            }
        }
        
    except Exception as e:
        logger.error(f"Error searching inventory by category: {str(e)}")
        return {
            "error": "Category search failed",
            "message": str(e),
            "category": category
        }


def get_low_stock_alerts(
    threshold: int = 10,
    region: Optional[str] = None,
    category: Optional[str] = None,
    index: str = "retail_store_inventory",
    size: int = 100
) -> Dict[str, Any]:
    """
    Identify products with low stock levels that need attention.
    
    Args:
        threshold: Inventory level threshold for low stock alert (default: 10)
        region: Optional region filter
        category: Optional category filter
        index: Elasticsearch index name
        size: Maximum number of results
    
    Returns:
        Dictionary containing low stock products and alert details
    """
    es = get_elasticsearch_client()
    if not es:
        return {"error": "Elasticsearch client not configured"}
    
    try:
        filters = [{
            "range": {
                "Inventory Level": {"lte": threshold}
            }
        }]
        
        if region:
            filters.append({"term": {"Region": region}})
        if category:
            filters.append({"multi_match": {
                "query": category,
                "fields": ["Category"]
            }})
        
        # Use standard search body instead of retriever + sort combination
        search_body = {
            "query": {
                "bool": {
                    "filter": filters
                }
            },
            "size": size,
            "sort": [{"Inventory Level": {"order": "asc"}}]
        }
        
        response = es.search(index=index, body=search_body)
        
        alerts = []
        critical_count = 0
        low_count = 0
        
        for hit in response['hits']['hits']:
            source = hit['_source']
            inventory = source.get('Inventory Level', 0)
            
            # Categorize alert severity
            if inventory == 0:
                severity = "critical"
                critical_count += 1
            elif inventory <= threshold / 2:
                severity = "high"
            else:
                severity = "medium"
                low_count += 1
            
            alerts.append({
                "severity": severity,
                "product_id": source.get('Product ID'),
                "store_id": source.get('Store ID'),
                "category": source.get('Category'),
                "region": source.get('Region'),
                "inventory_level": inventory,
                "units_sold": source.get('Units Sold', 0),
                "demand_forecast": source.get('Demand Forecast', 0),
                "date": source.get('Date')
            })
        
        return {
            "threshold": threshold,
            "total_alerts": len(alerts),
            "critical_alerts": critical_count,
            "low_stock_alerts": low_count,
            "alerts": alerts,
            "filters_applied": {
                "region": region,
                "category": category
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting low stock alerts: {str(e)}")
        return {
            "error": "Low stock alert query failed",
            "message": str(e)
        }


def get_inventory_by_region(
    region: str,
    category: Optional[str] = None,
    index: str = "retail_store_inventory",
    size: int = 100
) -> Dict[str, Any]:
    """
    Get inventory levels for a specific region.
    
    Args:
        region: Region to query (e.g., "North", "South", "East", "West")
        category: Optional category filter
        index: Elasticsearch index name
        size: Maximum number of results
    
    Returns:
        Dictionary containing regional inventory data
    """
    es = get_elasticsearch_client()
    if not es:
        return {"error": "Elasticsearch client not configured"}
    
    try:
        filters = [{"term": {"Region": region}}]
        
        if category:
            filters.append({"multi_match": {
                "query": category,
                "fields": ["Category"]
            }})
        
        retriever_object = {
            "standard": {
                "query": {
                    "bool": {
                        "filter": filters
                    }
                }
            }
        }
        
        response = es.search(
            index=index,
            retriever=retriever_object,
            size=size
        )
        
        # Aggregate regional data
        total_inventory = 0
        total_sold = 0
        stores = set()
        products_by_category = {}
        
        inventory_items = []
        
        for hit in response['hits']['hits']:
            source = hit['_source']
            inventory = source.get('Inventory Level', 0)
            sold = source.get('Units Sold', 0)
            cat = source.get('Category', 'Unknown')
            
            total_inventory += inventory
            total_sold += sold
            stores.add(source.get('Store ID'))
            
            if cat not in products_by_category:
                products_by_category[cat] = {
                    "inventory": 0,
                    "sold": 0,
                    "count": 0
                }
            
            products_by_category[cat]["inventory"] += inventory
            products_by_category[cat]["sold"] += sold
            products_by_category[cat]["count"] += 1
            
            inventory_items.append({
                "product_id": source.get('Product ID'),
                "store_id": source.get('Store ID'),
                "category": cat,
                "inventory_level": inventory,
                "units_sold": sold,
                "price": source.get('Price', 0),
                "date": source.get('Date')
            })
        
        return {
            "region": region,
            "total_inventory": total_inventory,
            "total_units_sold": total_sold,
            "store_count": len(stores),
            "stores": list(stores),
            "categories": products_by_category,
            "inventory_items": inventory_items,
            "total_results": response['hits']['total']['value']
        }
        
    except Exception as e:
        logger.error(f"Error getting regional inventory: {str(e)}")
        return {
            "error": "Regional inventory query failed",
            "message": str(e),
            "region": region
        }


def check_demand_forecast(
    product_id: Optional[str] = None,
    category: Optional[str] = None,
    region: Optional[str] = None,
    index: str = "retail_store_inventory",
    size: int = 50
) -> Dict[str, Any]:
    """
    Check demand forecasts for products to help with inventory planning.
    
    Args:
        product_id: Optional specific product ID
        category: Optional category filter
        region: Optional region filter
        index: Elasticsearch index name
        size: Maximum number of results
    
    Returns:
        Dictionary containing demand forecast data and recommendations
    """
    es = get_elasticsearch_client()
    if not es:
        return {"error": "Elasticsearch client not configured"}
    
    try:
        filters = []
        
        if product_id:
            filters.append({"term": {"Product ID": product_id}})
        if category:
            filters.append({"multi_match": {
                "query": category,
                "fields": ["Category"]
            }})
        if region:
            filters.append({"term": {"Region": region}})
        
        if not filters:
            return {
                "error": "At least one filter is required",
                "message": "Please specify product_id, category, or region"
            }
        
        retriever_object = {
            "standard": {
                "query": {
                    "bool": {
                        "filter": filters
                    }
                }
            }
        }
        
        response = es.search(
            index=index,
            retriever=retriever_object,
            size=size
        )
        
        forecasts = []
        restock_needed = []
        
        for hit in response['hits']['hits']:
            source = hit['_source']
            inventory = source.get('Inventory Level', 0)
            forecast = source.get('Demand Forecast', 0)
            
            # Calculate if restock is needed
            shortage = forecast - inventory
            needs_restock = shortage > 0
            
            forecast_data = {
                "product_id": source.get('Product ID'),
                "store_id": source.get('Store ID'),
                "category": source.get('Category'),
                "region": source.get('Region'),
                "current_inventory": inventory,
                "demand_forecast": forecast,
                "shortage": max(0, shortage),
                "needs_restock": needs_restock,
                "units_sold": source.get('Units Sold', 0),
                "units_ordered": source.get('Units Ordered', 0),
                "date": source.get('Date')
            }
            
            forecasts.append(forecast_data)
            
            if needs_restock:
                restock_needed.append(forecast_data)
        
        return {
            "total_products": len(forecasts),
            "restock_required": len(restock_needed),
            "forecasts": forecasts,
            "restock_recommendations": restock_needed,
            "filters_applied": {
                "product_id": product_id,
                "category": category,
                "region": region
            }
        }
        
    except Exception as e:
        logger.error(f"Error checking demand forecast: {str(e)}")
        return {
            "error": "Demand forecast query failed",
            "message": str(e)
        }


def get_seasonal_inventory_analysis(
    seasonality: str,
    region: Optional[str] = None,
    index: str = "retail_store_inventory",
    size: int = 100
) -> Dict[str, Any]:
    """
    Analyze inventory based on seasonal patterns.
    
    Args:
        seasonality: Season to analyze (e.g., "Summer", "Winter", "Spring", "Fall")
        region: Optional region filter
        index: Elasticsearch index name
        size: Maximum number of results
    
    Returns:
        Dictionary containing seasonal inventory analysis
    """
    es = get_elasticsearch_client()
    if not es:
        return {"error": "Elasticsearch client not configured"}
    
    try:
        filters = [{"term": {"Seasonality": seasonality}}]
        
        if region:
            filters.append({"term": {"Region": region}})
        
        retriever_object = {
            "standard": {
                "query": {
                    "bool": {
                        "filter": filters
                    }
                }
            }
        }
        
        response = es.search(
            index=index,
            retriever=retriever_object,
            size=size
        )
        
        # Aggregate seasonal data
        total_inventory = 0
        total_demand = 0
        categories = {}
        
        products = []
        
        for hit in response['hits']['hits']:
            source = hit['_source']
            inventory = source.get('Inventory Level', 0)
            demand = source.get('Demand Forecast', 0)
            cat = source.get('Category', 'Unknown')
            
            total_inventory += inventory
            total_demand += demand
            
            if cat not in categories:
                categories[cat] = {
                    "inventory": 0,
                    "demand": 0,
                    "products": 0
                }
            
            categories[cat]["inventory"] += inventory
            categories[cat]["demand"] += demand
            categories[cat]["products"] += 1
            
            products.append({
                "product_id": source.get('Product ID'),
                "store_id": source.get('Store ID'),
                "category": cat,
                "region": source.get('Region'),
                "inventory_level": inventory,
                "demand_forecast": demand,
                "units_sold": source.get('Units Sold', 0),
                "price": source.get('Price', 0),
                "discount": source.get('Discount', 0),
                "date": source.get('Date')
            })
        
        # Calculate readiness score
        readiness = (total_inventory / total_demand * 100) if total_demand > 0 else 0
        
        return {
            "seasonality": seasonality,
            "region": region,
            "total_inventory": total_inventory,
            "total_demand_forecast": total_demand,
            "readiness_score": round(readiness, 2),
            "readiness_status": "Ready" if readiness >= 100 else "Needs Restocking",
            "categories": categories,
            "products": products,
            "total_results": response['hits']['total']['value']
        }
        
    except Exception as e:
        logger.error(f"Error analyzing seasonal inventory: {str(e)}")
        return {
            "error": "Seasonal inventory analysis failed",
            "message": str(e),
            "seasonality": seasonality
        }


def get_inventory_statistics(
    index: str = "retail_store_inventory"
) -> Dict[str, Any]:
    """
    Get overall inventory statistics and aggregations.
    
    Args:
        index: Elasticsearch index name
    
    Returns:
        Dictionary containing comprehensive inventory statistics
    """
    es = get_elasticsearch_client()
    if not es:
        return {"error": "Elasticsearch client not configured"}
    
    try:
        search_body = {
            "size": 0,
            "aggs": {
                "total_inventory": {
                    "sum": {"field": "Inventory Level"}
                },
                "total_sold": {
                    "sum": {"field": "Units Sold"}
                },
                "total_ordered": {
                    "sum": {"field": "Units Ordered"}
                },
                "categories": {
                    "terms": {"field": "Category", "size": 50}
                },
                "regions": {
                    "terms": {"field": "Region", "size": 20}
                },
                "stores": {
                    "cardinality": {"field": "Store ID"}
                },
                "avg_inventory": {
                    "avg": {"field": "Inventory Level"}
                },
                "avg_price": {
                    "avg": {"field": "Price"}
                },
                "low_stock_count": {
                    "filter": {
                        "range": {
                            "Inventory Level": {"lte": 10}
                        }
                    }
                },
                "out_of_stock_count": {
                    "filter": {
                        "term": {
                            "Inventory Level": 0
                        }
                    }
                }
            }
        }
        
        response = es.search(index=index, body=search_body)
        aggs = response['aggregations']
        
        return {
            "total_products": response['hits']['total']['value'],
            "total_inventory": int(aggs['total_inventory']['value']),
            "total_units_sold": int(aggs['total_sold']['value']),
            "total_units_ordered": int(aggs['total_ordered']['value']),
            "unique_stores": aggs['stores']['value'],
            "average_inventory_per_product": round(aggs['avg_inventory']['value'], 2),
            "average_price": round(aggs['avg_price']['value'], 2),
            "low_stock_products": aggs['low_stock_count']['doc_count'],
            "out_of_stock_products": aggs['out_of_stock_count']['doc_count'],
            "categories": [
                {
                    "category": bucket['key'],
                    "product_count": bucket['doc_count']
                }
                for bucket in aggs['categories']['buckets']
            ],
            "regions": [
                {
                    "region": bucket['key'],
                    "product_count": bucket['doc_count']
                }
                for bucket in aggs['regions']['buckets']
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting inventory statistics: {str(e)}")
        return {
            "error": "Statistics query failed",
            "message": str(e)
        }
