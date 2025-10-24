"""
Shopping Agent Tools
Elasticsearch-based tools for analyzing customer shopping data and purchase patterns.
"""

import os
import logging
from typing import Dict, List, Any, Optional
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# Elasticsearch Configuration
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
        client = Elasticsearch(es_url, api_key=api_key)
        
        # Test connection
        if client.ping():
            logger.info("✅ Successfully connected to Elasticsearch")
        else:
            logger.warning("⚠️ Elasticsearch ping failed")
            
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Elasticsearch: {str(e)}")
        return None

# ============================================================================
# Shopping Data Analysis Tools
# ============================================================================

def search_shopping_data_by_category(
    category: str,
    size: int = 20
) -> Dict[str, Any]:
    """
    Search customer shopping data by product category.
    Analyzes purchase patterns, spending, and customer preferences.
    
    Args:
        category: Product category to search (e.g., "Clothing", "Shoes", "Technology")
        size: Number of results to return (default: 20)
    
    Returns:
        Dictionary containing shopping data and analytics
    """
    es = get_elasticsearch_client()
    if not es:
        return {
            "error": "Elasticsearch client not configured",
            "message": "Please check ELASTICSEARCH_CLOUD_URL and ELASTICSEARCH_API_KEY env vars"
        }
    
    try:
        # Search using multi_match on category field
        retriever_object = {
            "standard": {
                "query": {
                    "multi_match": {
                        "query": category,
                        "fields": ["category"],
                        "fuzziness": "AUTO"
                    }
                }
            }
        }
        
        response = es.search(
            index="customer_shopping_data.csv",
            retriever=retriever_object,
            size=size
        )
        
        hits = response['hits']['hits']
        total = response['hits']['total']['value']
        
        # Calculate analytics
        if hits:
            total_spending = sum(float(hit['_source'].get('price', 0)) * int(hit['_source'].get('quantity', 1)) 
                               for hit in hits)
            avg_price = sum(float(hit['_source'].get('price', 0)) for hit in hits) / len(hits)
            total_quantity = sum(int(hit['_source'].get('quantity', 1)) for hit in hits)
            
            # Get unique shopping malls
            malls = list(set(hit['_source'].get('shopping_mall', 'Unknown') for hit in hits))
            
            # Get payment methods used
            payment_methods = list(set(hit['_source'].get('payment_method', 'Unknown') for hit in hits))
            
            # Gender distribution
            gender_dist = {}
            for hit in hits:
                gender = hit['_source'].get('gender', 'Unknown')
                gender_dist[gender] = gender_dist.get(gender, 0) + 1
        else:
            total_spending = avg_price = total_quantity = 0
            malls = payment_methods = []
            gender_dist = {}
        
        return {
            "total_results": total,
            "results_shown": len(hits),
            "category": category,
            "analytics": {
                "total_spending": round(total_spending, 2),
                "average_price": round(avg_price, 2),
                "total_quantity": total_quantity,
                "unique_malls": len(malls),
                "malls": malls,
                "payment_methods": payment_methods,
                "gender_distribution": gender_dist
            },
            "transactions": [
                {
                    "invoice_no": hit['_source'].get('invoice_no'),
                    "customer_id": hit['_source'].get('customer_id'),
                    "gender": hit['_source'].get('gender'),
                    "age": hit['_source'].get('age'),
                    "category": hit['_source'].get('category'),
                    "quantity": hit['_source'].get('quantity'),
                    "price": hit['_source'].get('price'),
                    "payment_method": hit['_source'].get('payment_method'),
                    "invoice_date": hit['_source'].get('invoice_date'),
                    "shopping_mall": hit['_source'].get('shopping_mall')
                }
                for hit in hits
            ]
        }
        
    except Exception as e:
        logger.error(f"Error searching shopping data by category: {str(e)}")
        return {
            "error": "Search failed",
            "message": str(e),
            "category": category
        }


def get_customer_purchase_history(
    customer_id: str,
    size: int = 50
) -> Dict[str, Any]:
    """
    Retrieve complete purchase history for a specific customer.
    
    Args:
        customer_id: Customer ID to lookup
        size: Maximum number of transactions to return (default: 50)
    
    Returns:
        Dictionary containing customer's purchase history and analytics
    """
    es = get_elasticsearch_client()
    if not es:
        return {
            "error": "Elasticsearch client not configured",
            "message": "Please check ELASTICSEARCH_CLOUD_URL and ELASTICSEARCH_API_KEY env vars"
        }
    
    try:
        response = es.search(
            index="customer_shopping_data.csv",
            body={
                "query": {
                    "term": {
                        "customer_id": customer_id
                    }
                },
                "sort": [
                    {"invoice_date": {"order": "desc"}}
                ],
                "size": size
            }
        )
        
        hits = response['hits']['hits']
        total = response['hits']['total']['value']
        
        if not hits:
            return {
                "customer_id": customer_id,
                "total_purchases": 0,
                "message": "No purchase history found for this customer"
            }
        
        # Calculate customer analytics
        total_spent = sum(float(hit['_source'].get('price', 0)) * int(hit['_source'].get('quantity', 1)) 
                         for hit in hits)
        total_items = sum(int(hit['_source'].get('quantity', 1)) for hit in hits)
        
        # Category preferences
        categories = {}
        for hit in hits:
            cat = hit['_source'].get('category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        # Shopping mall preferences
        malls = {}
        for hit in hits:
            mall = hit['_source'].get('shopping_mall', 'Unknown')
            malls[mall] = malls.get(mall, 0) + 1
        
        # Payment method preferences
        payment_methods = {}
        for hit in hits:
            pm = hit['_source'].get('payment_method', 'Unknown')
            payment_methods[pm] = payment_methods.get(pm, 0) + 1
        
        # Get customer demographics from most recent purchase
        latest = hits[0]['_source']
        
        return {
            "customer_id": customer_id,
            "total_purchases": total,
            "purchases_shown": len(hits),
            "customer_profile": {
                "gender": latest.get('gender'),
                "age": latest.get('age')
            },
            "spending_analytics": {
                "total_spent": round(total_spent, 2),
                "average_transaction": round(total_spent / len(hits), 2) if hits else 0,
                "total_items_purchased": total_items,
                "average_items_per_transaction": round(total_items / len(hits), 2) if hits else 0
            },
            "preferences": {
                "favorite_categories": sorted(categories.items(), key=lambda x: x[1], reverse=True),
                "favorite_malls": sorted(malls.items(), key=lambda x: x[1], reverse=True),
                "payment_methods": sorted(payment_methods.items(), key=lambda x: x[1], reverse=True)
            },
            "purchase_history": [
                {
                    "invoice_no": hit['_source'].get('invoice_no'),
                    "date": hit['_source'].get('invoice_date'),
                    "category": hit['_source'].get('category'),
                    "quantity": hit['_source'].get('quantity'),
                    "price": hit['_source'].get('price'),
                    "total": round(float(hit['_source'].get('price', 0)) * int(hit['_source'].get('quantity', 1)), 2),
                    "payment_method": hit['_source'].get('payment_method'),
                    "shopping_mall": hit['_source'].get('shopping_mall')
                }
                for hit in hits
            ]
        }
        
    except Exception as e:
        logger.error(f"Error retrieving customer purchase history: {str(e)}")
        return {
            "error": "Search failed",
            "message": str(e),
            "customer_id": customer_id
        }


def analyze_shopping_trends_by_gender(
    gender: str,
    size: int = 100
) -> Dict[str, Any]:
    """
    Analyze shopping trends and preferences by gender.
    
    Args:
        gender: Gender to analyze (e.g., "Male", "Female")
        size: Sample size for analysis (default: 100)
    
    Returns:
        Dictionary containing gender-based shopping trends
    """
    es = get_elasticsearch_client()
    if not es:
        return {
            "error": "Elasticsearch client not configured",
            "message": "Please check ELASTICSEARCH_CLOUD_URL and ELASTICSEARCH_API_KEY env vars"
        }
    
    try:
        response = es.search(
            index="customer_shopping_data.csv",
            body={
                "query": {
                    "term": {
                        "gender": gender
                    }
                },
                "size": size,
                "aggs": {
                    "categories": {
                        "terms": {
                            "field": "category",
                            "size": 20
                        },
                        "aggs": {
                            "avg_price": {"avg": {"field": "price"}},
                            "total_quantity": {"sum": {"field": "quantity"}}
                        }
                    },
                    "payment_methods": {
                        "terms": {
                            "field": "payment_method",
                            "size": 10
                        }
                    },
                    "shopping_malls": {
                        "terms": {
                            "field": "shopping_mall",
                            "size": 10
                        }
                    },
                    "avg_age": {
                        "avg": {"field": "age"}
                    },
                    "avg_price": {
                        "avg": {"field": "price"}
                    },
                    "total_spent": {
                        "sum": {
                            "script": {
                                "source": "doc['price'].value * doc['quantity'].value"
                            }
                        }
                    }
                }
            }
        )
        
        total = response['hits']['total']['value']
        aggs = response['aggregations']
        
        return {
            "gender": gender,
            "total_transactions": total,
            "sample_size": len(response['hits']['hits']),
            "demographics": {
                "average_age": round(aggs['avg_age']['value'], 1) if aggs['avg_age']['value'] else 0
            },
            "spending_patterns": {
                "average_price": round(aggs['avg_price']['value'], 2) if aggs['avg_price']['value'] else 0,
                "total_spending": round(aggs['total_spent']['value'], 2) if aggs['total_spent']['value'] else 0
            },
            "category_preferences": [
                {
                    "category": bucket['key'],
                    "purchase_count": bucket['doc_count'],
                    "avg_price": round(bucket['avg_price']['value'], 2),
                    "total_quantity": int(bucket['total_quantity']['value'])
                }
                for bucket in aggs['categories']['buckets']
            ],
            "payment_preferences": [
                {
                    "payment_method": bucket['key'],
                    "usage_count": bucket['doc_count']
                }
                for bucket in aggs['payment_methods']['buckets']
            ],
            "shopping_mall_preferences": [
                {
                    "mall": bucket['key'],
                    "visit_count": bucket['doc_count']
                }
                for bucket in aggs['shopping_malls']['buckets']
            ]
        }
        
    except Exception as e:
        logger.error(f"Error analyzing shopping trends by gender: {str(e)}")
        return {
            "error": "Analysis failed",
            "message": str(e),
            "gender": gender
        }


def get_high_value_transactions(
    min_amount: float = 100.0,
    size: int = 20
) -> Dict[str, Any]:
    """
    Find high-value transactions above a specified amount.
    
    Args:
        min_amount: Minimum transaction amount (default: 100.0)
        size: Number of results to return (default: 20)
    
    Returns:
        Dictionary containing high-value transactions
    """
    es = get_elasticsearch_client()
    if not es:
        return {
            "error": "Elasticsearch client not configured",
            "message": "Please check ELASTICSEARCH_CLOUD_URL and ELASTICSEARCH_API_KEY env vars"
        }
    
    try:
        response = es.search(
            index="customer_shopping_data.csv",
            body={
                "query": {
                    "script": {
                        "script": {
                            "source": "doc['price'].value * doc['quantity'].value >= params.min_amount",
                            "params": {
                                "min_amount": min_amount
                            }
                        }
                    }
                },
                "sort": [
                    {
                        "_script": {
                            "type": "number",
                            "script": {
                                "source": "doc['price'].value * doc['quantity'].value"
                            },
                            "order": "desc"
                        }
                    }
                ],
                "size": size
            }
        )
        
        hits = response['hits']['hits']
        total = response['hits']['total']['value']
        
        transactions = []
        for hit in hits:
            source = hit['_source']
            price = float(source.get('price', 0))
            quantity = int(source.get('quantity', 1))
            total_amount = price * quantity
            
            transactions.append({
                "invoice_no": source.get('invoice_no'),
                "customer_id": source.get('customer_id'),
                "date": source.get('invoice_date'),
                "category": source.get('category'),
                "quantity": quantity,
                "unit_price": price,
                "total_amount": round(total_amount, 2),
                "payment_method": source.get('payment_method'),
                "shopping_mall": source.get('shopping_mall'),
                "customer_age": source.get('age'),
                "customer_gender": source.get('gender')
            })
        
        total_value = sum(t['total_amount'] for t in transactions)
        avg_value = total_value / len(transactions) if transactions else 0
        
        return {
            "threshold": min_amount,
            "total_matching": total,
            "transactions_shown": len(transactions),
            "analytics": {
                "total_value": round(total_value, 2),
                "average_value": round(avg_value, 2),
                "highest_transaction": round(transactions[0]['total_amount'], 2) if transactions else 0
            },
            "transactions": transactions
        }
        
    except Exception as e:
        logger.error(f"Error retrieving high-value transactions: {str(e)}")
        return {
            "error": "Search failed",
            "message": str(e),
            "min_amount": min_amount
        }


def analyze_shopping_mall_performance(
    shopping_mall: Optional[str] = None,
    size: int = 50
) -> Dict[str, Any]:
    """
    Analyze shopping mall performance and customer traffic.
    
    Args:
        shopping_mall: Specific mall to analyze (None for all malls comparison)
        size: Sample size for analysis (default: 50)
    
    Returns:
        Dictionary containing mall performance metrics
    """
    es = get_elasticsearch_client()
    if not es:
        return {
            "error": "Elasticsearch client not configured",
            "message": "Please check ELASTICSEARCH_CLOUD_URL and ELASTICSEARCH_API_KEY env vars"
        }
    
    try:
        if shopping_mall:
            # Analyze specific mall
            query = {"term": {"shopping_mall": shopping_mall}}
        else:
            # Analyze all malls
            query = {"match_all": {}}
        
        response = es.search(
            index="customer_shopping_data.csv",
            body={
                "query": query,
                "size": size,
                "aggs": {
                    "malls": {
                        "terms": {
                            "field": "shopping_mall",
                            "size": 20
                        },
                        "aggs": {
                            "revenue": {
                                "sum": {
                                    "script": {
                                        "source": "doc['price'].value * doc['quantity'].value"
                                    }
                                }
                            },
                            "avg_transaction": {
                                "avg": {
                                    "script": {
                                        "source": "doc['price'].value * doc['quantity'].value"
                                    }
                                }
                            },
                            "categories": {
                                "terms": {
                                    "field": "category",
                                    "size": 10
                                }
                            },
                            "payment_methods": {
                                "terms": {
                                    "field": "payment_method",
                                    "size": 5
                                }
                            },
                            "avg_customer_age": {
                                "avg": {"field": "age"}
                            }
                        }
                    }
                }
            }
        )
        
        mall_stats = []
        for bucket in response['aggregations']['malls']['buckets']:
            mall_stats.append({
                "mall_name": bucket['key'],
                "total_transactions": bucket['doc_count'],
                "total_revenue": round(bucket['revenue']['value'], 2),
                "average_transaction_value": round(bucket['avg_transaction']['value'], 2),
                "average_customer_age": round(bucket['avg_customer_age']['value'], 1),
                "top_categories": [
                    {"category": cat['key'], "count": cat['doc_count']}
                    for cat in bucket['categories']['buckets'][:5]
                ],
                "payment_methods": [
                    {"method": pm['key'], "count": pm['doc_count']}
                    for pm in bucket['payment_methods']['buckets']
                ]
            })
        
        # Sort by revenue
        mall_stats.sort(key=lambda x: x['total_revenue'], reverse=True)
        
        return {
            "analysis_type": "specific_mall" if shopping_mall else "all_malls",
            "mall_filter": shopping_mall,
            "total_malls_analyzed": len(mall_stats),
            "mall_performance": mall_stats,
            "summary": {
                "highest_revenue_mall": mall_stats[0]['mall_name'] if mall_stats else None,
                "total_combined_revenue": round(sum(m['total_revenue'] for m in mall_stats), 2),
                "total_transactions": sum(m['total_transactions'] for m in mall_stats)
            }
        }
        
    except Exception as e:
        logger.error(f"Error analyzing shopping mall performance: {str(e)}")
        return {
            "error": "Analysis failed",
            "message": str(e),
            "shopping_mall": shopping_mall
        }


def get_payment_method_analytics(
    size: int = 100
) -> Dict[str, Any]:
    """
    Analyze payment method usage patterns and preferences.
    
    Args:
        size: Sample size for analysis (default: 100)
    
    Returns:
        Dictionary containing payment method analytics
    """
    es = get_elasticsearch_client()
    if not es:
        return {
            "error": "Elasticsearch client not configured",
            "message": "Please check ELASTICSEARCH_CLOUD_URL and ELASTICSEARCH_API_KEY env vars"
        }
    
    try:
        response = es.search(
            index="customer_shopping_data.csv",
            body={
                "query": {"match_all": {}},
                "size": 0,
                "aggs": {
                    "payment_methods": {
                        "terms": {
                            "field": "payment_method",
                            "size": 10
                        },
                        "aggs": {
                            "total_revenue": {
                                "sum": {
                                    "script": {
                                        "source": "doc['price'].value * doc['quantity'].value"
                                    }
                                }
                            },
                            "avg_transaction": {
                                "avg": {
                                    "script": {
                                        "source": "doc['price'].value * doc['quantity'].value"
                                    }
                                }
                            },
                            "gender_distribution": {
                                "terms": {
                                    "field": "gender"
                                }
                            },
                            "age_stats": {
                                "stats": {"field": "age"}
                            }
                        }
                    }
                }
            }
        )
        
        payment_stats = []
        for bucket in response['aggregations']['payment_methods']['buckets']:
            payment_stats.append({
                "payment_method": bucket['key'],
                "transaction_count": bucket['doc_count'],
                "total_revenue": round(bucket['total_revenue']['value'], 2),
                "average_transaction_value": round(bucket['avg_transaction']['value'], 2),
                "gender_distribution": [
                    {"gender": g['key'], "count": g['doc_count']}
                    for g in bucket['gender_distribution']['buckets']
                ],
                "customer_age_stats": {
                    "average": round(bucket['age_stats']['avg'], 1),
                    "min": bucket['age_stats']['min'],
                    "max": bucket['age_stats']['max']
                }
            })
        
        # Sort by usage
        payment_stats.sort(key=lambda x: x['transaction_count'], reverse=True)
        
        total_transactions = sum(p['transaction_count'] for p in payment_stats)
        total_revenue = sum(p['total_revenue'] for p in payment_stats)
        
        # Calculate percentages
        for stat in payment_stats:
            stat['usage_percentage'] = round((stat['transaction_count'] / total_transactions * 100), 2) if total_transactions > 0 else 0
            stat['revenue_percentage'] = round((stat['total_revenue'] / total_revenue * 100), 2) if total_revenue > 0 else 0
        
        return {
            "total_transactions_analyzed": total_transactions,
            "total_revenue": round(total_revenue, 2),
            "payment_methods_count": len(payment_stats),
            "payment_method_analytics": payment_stats,
            "most_popular_method": payment_stats[0]['payment_method'] if payment_stats else None,
            "highest_revenue_method": max(payment_stats, key=lambda x: x['total_revenue'])['payment_method'] if payment_stats else None
        }
        
    except Exception as e:
        logger.error(f"Error analyzing payment methods: {str(e)}")
        return {
            "error": "Analysis failed",
            "message": str(e)
        }


def search_transactions_by_date_range(
    start_date: str,
    end_date: str,
    size: int = 50
) -> Dict[str, Any]:
    """
    Search transactions within a specific date range.
    
    Args:
        start_date: Start date in format YYYY-MM-DD or DD/MM/YYYY
        end_date: End date in format YYYY-MM-DD or DD/MM/YYYY
        size: Number of results to return (default: 50)
    
    Returns:
        Dictionary containing transactions within the date range
    """
    es = get_elasticsearch_client()
    if not es:
        return {
            "error": "Elasticsearch client not configured",
            "message": "Please check ELASTICSEARCH_CLOUD_URL and ELASTICSEARCH_API_KEY env vars"
        }
    
    try:
        # Convert date format if needed (YYYY-MM-DD to DD/MM/YYYY)
        from datetime import datetime
        
        # Parse and convert dates
        try:
            if '-' in start_date:  # YYYY-MM-DD format
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                start_formatted = start_dt.strftime("%d/%m/%Y")
            else:
                start_formatted = start_date
                
            if '-' in end_date:  # YYYY-MM-DD format
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                end_formatted = end_dt.strftime("%d/%m/%Y")
            else:
                end_formatted = end_date
        except ValueError:
            # If parsing fails, use original dates
            start_formatted = start_date
            end_formatted = end_date
        
        response = es.search(
            index="customer_shopping_data.csv",
            body={
                "query": {
                    "range": {
                        "invoice_date": {
                            "gte": start_formatted,
                            "lte": end_formatted
                        }
                    }
                },
                "sort": [
                    {"invoice_date": {"order": "desc"}}
                ],
                "size": size,
                "aggs": {
                    "total_revenue": {
                        "sum": {
                            "script": {
                                "source": "doc['price'].value * doc['quantity'].value"
                            }
                        }
                    },
                    "categories": {
                        "terms": {
                            "field": "category",
                            "size": 10
                        }
                    },
                    "dates": {
                        "terms": {
                            "field": "invoice_date",
                            "size": 365,
                            "order": {"_key": "asc"}
                        },
                        "aggs": {
                            "daily_revenue": {
                                "sum": {
                                    "script": {
                                        "source": "doc['price'].value * doc['quantity'].value"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        )
        
        hits = response['hits']['hits']
        total = response['hits']['total']['value']
        aggs = response['aggregations']
        
        return {
            "date_range": {
                "start": start_date,
                "end": end_date
            },
            "total_transactions": total,
            "transactions_shown": len(hits),
            "analytics": {
                "total_revenue": round(aggs['total_revenue']['value'], 2),
                "average_transaction": round(aggs['total_revenue']['value'] / total, 2) if total > 0 else 0,
                "top_categories": [
                    {"category": bucket['key'], "count": bucket['doc_count']}
                    for bucket in aggs['categories']['buckets']
                ],
                "daily_sales": [
                    {
                        "date": bucket['key'],
                        "transaction_count": bucket['doc_count'],
                        "revenue": round(bucket['daily_revenue']['value'], 2)
                    }
                    for bucket in aggs['dates']['buckets']
                ]
            },
            "transactions": [
                {
                    "invoice_no": hit['_source'].get('invoice_no'),
                    "date": hit['_source'].get('invoice_date'),
                    "customer_id": hit['_source'].get('customer_id'),
                    "category": hit['_source'].get('category'),
                    "quantity": hit['_source'].get('quantity'),
                    "price": hit['_source'].get('price'),
                    "total": round(float(hit['_source'].get('price', 0)) * int(hit['_source'].get('quantity', 1)), 2),
                    "payment_method": hit['_source'].get('payment_method'),
                    "shopping_mall": hit['_source'].get('shopping_mall')
                }
                for hit in hits
            ]
        }
        
    except Exception as e:
        logger.error(f"Error searching transactions by date range: {str(e)}")
        return {
            "error": "Search failed",
            "message": str(e),
            "date_range": {"start": start_date, "end": end_date}
        }
