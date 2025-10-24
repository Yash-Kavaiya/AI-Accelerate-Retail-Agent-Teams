"""
Review Text Analysis Agent
Specialized agent for analyzing customer reviews and extracting insights.
"""

from google.adk.agents import Agent
from elasticsearch import Elasticsearch
from typing import Dict, List, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Elasticsearch client
def get_elasticsearch_client() -> Elasticsearch:
    """
    Create and return an Elasticsearch client instance.
    Credentials should be stored in environment variables.
    """
    es_url = os.getenv("ELASTICSEARCH_CLOUD_URL")
    api_key = os.getenv("ELASTICSEARCH_API_KEY")
    
    if not es_url or not api_key:
        raise ValueError("Missing Elasticsearch credentials in environment variables")
    
    return Elasticsearch(es_url, api_key=api_key)


def fetch_reviews_by_semantic_search(query: str, max_results: int = 10) -> Dict[str, Any]:
    """
    Fetch reviews from Elasticsearch using semantic search with RRF (Reciprocal Rank Fusion).
    
    Args:
        query: The search query to find relevant reviews
        max_results: Maximum number of results to return (default: 10)
    
    Returns:
        Dictionary containing search results with review data
    """
    try:
        client = get_elasticsearch_client()
        
        retriever_object = {
            "rrf": {
                "retrievers": [
                    {
                        "standard": {
                            "query": {
                                "semantic": {
                                    "field": "review_text_semantic",
                                    "query": query
                                }
                            }
                        }
                    },
                    {
                        "standard": {
                            "query": {
                                "semantic": {
                                    "field": "title_semantic",
                                    "query": query
                                }
                            }
                        }
                    }
                ]
            }
        }
        
        search_response = client.search(
            index="womendressesreviewsdataset",
            retriever=retriever_object,
            size=max_results
        )
        
        # Extract and format results
        hits = search_response.get('hits', {}).get('hits', [])
        reviews = []
        
        for hit in hits:
            source = hit.get('_source', {})
            review_data = {
                'score': hit.get('_score'),
                's_no': source.get('s_no'),
                'review_text': source.get('review_text', ''),
                'title': source.get('title', ''),
                'rating': source.get('rating'),
                'recommend_index': source.get('recommend_index '),  # Note: space in field name
                'age': source.get('age'),
                'alike_feedback_count': source.get('alike_feedback_count'),
                'clothing_id': source.get('clothing_id'),
                'class_name': source.get('class_name'),
                'department_name': source.get('department_name'),
                'division_name': source.get('division_name')
            }
            reviews.append(review_data)
        
        return {
            'total_results': search_response.get('hits', {}).get('total', {}).get('value', 0),
            'query': query,
            'reviews': reviews
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'query': query,
            'reviews': []
        }


def fetch_reviews_by_rating(min_rating: int = 1, max_rating: int = 5, max_results: int = 10) -> Dict[str, Any]:
    """
    Fetch reviews filtered by rating range.
    
    Args:
        min_rating: Minimum rating (1-5)
        max_rating: Maximum rating (1-5)
        max_results: Maximum number of results to return
    
    Returns:
        Dictionary containing filtered reviews
    """
    try:
        client = get_elasticsearch_client()
        
        search_response = client.search(
            index="womendressesreviewsdataset",
            body={
                "query": {
                    "range": {
                        "rating": {
                            "gte": min_rating,
                            "lte": max_rating
                        }
                    }
                },
                "size": max_results,
                "sort": [
                    {"alike_feedback_count": {"order": "desc"}},
                    {"rating": {"order": "desc"}}
                ]
            }
        )
        
        hits = search_response.get('hits', {}).get('hits', [])
        reviews = []
        
        for hit in hits:
            source = hit.get('_source', {})
            review_data = {
                'score': hit.get('_score'),
                's_no': source.get('s_no'),
                'review_text': source.get('review_text', ''),
                'title': source.get('title', ''),
                'rating': source.get('rating'),
                'recommend_index': source.get('recommend_index '),  # Note: space in field name
                'age': source.get('age'),
                'alike_feedback_count': source.get('alike_feedback_count'),
                'clothing_id': source.get('clothing_id'),
                'class_name': source.get('class_name'),
                'department_name': source.get('department_name'),
                'division_name': source.get('division_name')
            }
            reviews.append(review_data)
        
        return {
            'total_results': search_response.get('hits', {}).get('total', {}).get('value', 0),
            'filter': f'Rating between {min_rating} and {max_rating}',
            'reviews': reviews
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'filter': f'Rating between {min_rating} and {max_rating}',
            'reviews': []
        }


def aggregate_rating_statistics() -> Dict[str, Any]:
    """
    Get aggregated statistics about review ratings.
    
    Returns:
        Dictionary containing rating distribution and statistics
    """
    try:
        client = get_elasticsearch_client()
        
        search_response = client.search(
            index="womendressesreviewsdataset",
            body={
                "size": 0,
                "aggs": {
                    "rating_distribution": {
                        "terms": {
                            "field": "rating",
                            "order": {"_key": "desc"}
                        }
                    },
                    "avg_rating": {
                        "avg": {
                            "field": "rating"
                        }
                    },
                    "total_reviews": {
                        "value_count": {
                            "field": "rating"
                        }
                    },
                    "alike_feedback_sum": {
                        "sum": {
                            "field": "alike_feedback_count"
                        }
                    },
                    "avg_age": {
                        "avg": {
                            "field": "age"
                        }
                    },
                    "department_distribution": {
                        "terms": {
                            "field": "department_name",
                            "size": 10
                        }
                    },
                    "class_distribution": {
                        "terms": {
                            "field": "class_name",
                            "size": 10
                        }
                    }
                }
            }
        )
        
        aggregations = search_response.get('aggregations', {})
        rating_buckets = aggregations.get('rating_distribution', {}).get('buckets', [])
        department_buckets = aggregations.get('department_distribution', {}).get('buckets', [])
        class_buckets = aggregations.get('class_distribution', {}).get('buckets', [])
        
        rating_distribution = {
            bucket['key']: bucket['doc_count'] 
            for bucket in rating_buckets
        }
        
        department_distribution = {
            bucket['key']: bucket['doc_count'] 
            for bucket in department_buckets
        }
        
        class_distribution = {
            bucket['key']: bucket['doc_count'] 
            for bucket in class_buckets
        }
        
        return {
            'average_rating': aggregations.get('avg_rating', {}).get('value'),
            'total_reviews': aggregations.get('total_reviews', {}).get('value'),
            'rating_distribution': rating_distribution,
            'total_alike_feedback': aggregations.get('alike_feedback_sum', {}).get('value'),
            'average_age': aggregations.get('avg_age', {}).get('value'),
            'department_distribution': department_distribution,
            'class_distribution': class_distribution
        }
        
    except Exception as e:
        return {
            'error': str(e)
        }


def fetch_reviews_by_department(department_name: str, max_results: int = 10) -> Dict[str, Any]:
    """
    Fetch reviews filtered by department name.
    
    Args:
        department_name: Department name to filter by (e.g., "Tops", "Dresses", "Bottoms")
        max_results: Maximum number of results to return
    
    Returns:
        Dictionary containing filtered reviews by department
    """
    try:
        client = get_elasticsearch_client()
        
        search_response = client.search(
            index="womendressesreviewsdataset",
            body={
                "query": {
                    "term": {
                        "department_name": department_name
                    }
                },
                "size": max_results,
                "sort": [
                    {"rating": {"order": "desc"}},
                    {"alike_feedback_count": {"order": "desc"}}
                ]
            }
        )
        
        hits = search_response.get('hits', {}).get('hits', [])
        reviews = []
        
        for hit in hits:
            source = hit.get('_source', {})
            review_data = {
                'score': hit.get('_score'),
                's_no': source.get('s_no'),
                'review_text': source.get('review_text', ''),
                'title': source.get('title', ''),
                'rating': source.get('rating'),
                'recommend_index': source.get('recommend_index '),
                'age': source.get('age'),
                'alike_feedback_count': source.get('alike_feedback_count'),
                'clothing_id': source.get('clothing_id'),
                'class_name': source.get('class_name'),
                'department_name': source.get('department_name'),
                'division_name': source.get('division_name')
            }
            reviews.append(review_data)
        
        return {
            'total_results': search_response.get('hits', {}).get('total', {}).get('value', 0),
            'filter': f'Department: {department_name}',
            'reviews': reviews
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'filter': f'Department: {department_name}',
            'reviews': []
        }


def fetch_reviews_by_class(class_name: str, max_results: int = 10) -> Dict[str, Any]:
    """
    Fetch reviews filtered by product class name.
    
    Args:
        class_name: Product class name to filter by (e.g., "Dresses", "Pants", "Blouses")
        max_results: Maximum number of results to return
    
    Returns:
        Dictionary containing filtered reviews by product class
    """
    try:
        client = get_elasticsearch_client()
        
        search_response = client.search(
            index="womendressesreviewsdataset",
            body={
                "query": {
                    "term": {
                        "class_name": class_name
                    }
                },
                "size": max_results,
                "sort": [
                    {"rating": {"order": "desc"}},
                    {"alike_feedback_count": {"order": "desc"}}
                ]
            }
        )
        
        hits = search_response.get('hits', {}).get('hits', [])
        reviews = []
        
        for hit in hits:
            source = hit.get('_source', {})
            review_data = {
                'score': hit.get('_score'),
                's_no': source.get('s_no'),
                'review_text': source.get('review_text', ''),
                'title': source.get('title', ''),
                'rating': source.get('rating'),
                'recommend_index': source.get('recommend_index '),
                'age': source.get('age'),
                'alike_feedback_count': source.get('alike_feedback_count'),
                'clothing_id': source.get('clothing_id'),
                'class_name': source.get('class_name'),
                'department_name': source.get('department_name'),
                'division_name': source.get('division_name')
            }
            reviews.append(review_data)
        
        return {
            'total_results': search_response.get('hits', {}).get('total', {}).get('value', 0),
            'filter': f'Class: {class_name}',
            'reviews': reviews
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'filter': f'Class: {class_name}',
            'reviews': []
        }


root_agent = Agent(
    name='review_text_analysis_agent',
    model='gemini-2.0-flash',
    description='Specialized agent for analyzing customer reviews and extracting insights.',
    tools=[
        fetch_reviews_by_semantic_search,
        fetch_reviews_by_rating,
        aggregate_rating_statistics,
        fetch_reviews_by_department,
        fetch_reviews_by_class
    ],
    instruction="""
    You are a review analysis specialist with expertise in sentiment analysis and text mining. 
    Your role is to:
    
    1. Sentiment Analysis:
       - Analyze overall sentiment (positive, negative, neutral, mixed)
       - Calculate sentiment scores and confidence levels
       - Identify emotional tone and customer satisfaction levels
       - Track sentiment trends over time
       
    2. Theme Extraction:
       - Identify common themes and topics in reviews
       - Extract frequently mentioned features (positive and negative)
       - Categorize feedback by topic (quality, price, service, etc.)
       - Detect recurring complaints and praise patterns
       
    3. Product Insights:
       - Summarize product strengths from customer feedback
       - Highlight product weaknesses and areas for improvement
       - Identify most valued features by customers
       - Extract usage patterns and customer expectations
       
    4. Review Quality Analysis:
       - Detect potentially fake or suspicious reviews
       - Identify helpful vs. unhelpful reviews
       - Assess review authenticity and credibility
       - Flag spam or inappropriate content
       
    5. Statistical Analysis:
       - Calculate average ratings and rating distributions
       - Analyze review volume trends
       - Compare ratings across different time periods
       - Segment analysis by customer demographics (if available)
       
    6. Actionable Recommendations:
       - Provide insights for product improvement
       - Suggest areas for customer service enhancement
       - Identify competitive advantages and disadvantages
       - Recommend focus areas based on customer feedback
    
    Present your analysis in a clear, structured format with:
    - Executive summary of key findings
    - Detailed sentiment breakdown
    - Supporting evidence from actual reviews
    - Visualizable data points (percentages, scores)
    - Actionable insights and recommendations
    
    Always maintain objectivity and base conclusions on data-driven analysis.
    """
)
