"""
Customer Support Agent
Specialized agent for handling customer inquiries, issues, and support requests.
"""

import os
import logging
from typing import Dict, List, Any, Optional
from elasticsearch import Elasticsearch
from google.adk.agents import Agent
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from the retail-agents-team directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

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
        
        logger.info(f"Connecting to Elasticsearch for FAQs...")
        return Elasticsearch(es_url, api_key=api_key)
    except Exception as e:
        logger.error(f"Failed to connect to Elasticsearch: {str(e)}")
        return None


# ============================================================================
# FAQ and Support Documentation Search Functions
# ============================================================================

def search_faqs(
    query: str,
    index: str = "faqs_data",
    size: int = 5
) -> Dict[str, Any]:
    """
    Search FAQ documents using full-text search on content.
    
    Args:
        query: Search query (customer question or keywords)
        index: Elasticsearch index name for FAQs
        size: Number of results to return (default: 5)
    
    Returns:
        Dictionary containing relevant FAQ documents with content
    """
    es = get_elasticsearch_client()
    if not es:
        return {
            "error": "Elasticsearch client not configured",
            "message": "Please check ELASTICSEARCH_CLOUD_URL and ELASTICSEARCH_API_KEY env vars",
            "query": query
        }
    
    try:
        retriever_object = {
            "standard": {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["attachment.content"]
                    }
                }
            }
        }
        
        response = es.search(
            index=index,
            retriever=retriever_object,
            size=size
        )
        
        # Extract and format results
        faqs = []
        for hit in response['hits']['hits']:
            attachment = hit['_source'].get('attachment', {})
            faq_data = {
                'id': hit['_id'],
                'score': hit['_score'],
                'content': attachment.get('content', ''),
                'content_length': attachment.get('content_length'),
                'content_type': attachment.get('content_type'),
                'language': attachment.get('language'),
                'format': attachment.get('format'),
                'creator_tool': attachment.get('creator_tool'),
                'date': attachment.get('date'),
                'modified': attachment.get('modified')
            }
            faqs.append(faq_data)
        
        return {
            'total_results': response['hits']['total']['value'],
            'query': query,
            'faqs': faqs
        }
        
    except Exception as e:
        logger.error(f"FAQ search error: {str(e)}")
        return {
            'error': 'FAQ search failed',
            'message': str(e),
            'query': query,
            'faqs': []
        }


def search_faqs_by_topic(
    topic: str,
    keywords: Optional[List[str]] = None,
    index: str = "faqs_data",
    size: int = 10
) -> Dict[str, Any]:
    """
    Search FAQs by topic with optional additional keywords.
    
    Args:
        topic: Main topic (e.g., "returns", "shipping", "warranty")
        keywords: Additional keywords to refine search
        index: Elasticsearch index name
        size: Number of results to return
    
    Returns:
        Dictionary containing topic-relevant FAQs
    """
    es = get_elasticsearch_client()
    if not es:
        return {
            "error": "Elasticsearch client not configured",
            "query": topic
        }
    
    try:
        # Build search query
        search_terms = [topic]
        if keywords:
            search_terms.extend(keywords)
        
        query_string = " ".join(search_terms)
        
        retriever_object = {
            "standard": {
                "query": {
                    "multi_match": {
                        "query": query_string,
                        "fields": ["attachment.content"],
                        "type": "best_fields",
                        "fuzziness": "AUTO"
                    }
                }
            }
        }
        
        response = es.search(
            index=index,
            retriever=retriever_object,
            size=size
        )
        
        faqs = []
        for hit in response['hits']['hits']:
            attachment = hit['_source'].get('attachment', {})
            faqs.append({
                'id': hit['_id'],
                'score': hit['_score'],
                'content': attachment.get('content', ''),
                'content_length': attachment.get('content_length'),
                'content_type': attachment.get('content_type'),
                'language': attachment.get('language'),
                'date': attachment.get('date'),
                'modified': attachment.get('modified')
            })
        
        return {
            'total_results': response['hits']['total']['value'],
            'topic': topic,
            'keywords': keywords or [],
            'faqs': faqs
        }
        
    except Exception as e:
        logger.error(f"Topic search error: {str(e)}")
        return {
            'error': 'Topic search failed',
            'message': str(e),
            'topic': topic,
            'faqs': []
        }


def get_faq_by_id(
    faq_id: str,
    index: str = "faqs_data"
) -> Dict[str, Any]:
    """
    Retrieve a specific FAQ document by its ID.
    
    Args:
        faq_id: Elasticsearch document ID
        index: Elasticsearch index name
    
    Returns:
        Dictionary containing complete FAQ document
    """
    es = get_elasticsearch_client()
    if not es:
        return {"error": "Elasticsearch client not configured"}
    
    try:
        response = es.get(index=index, id=faq_id)
        attachment = response['_source'].get('attachment', {})
        
        return {
            'id': response['_id'],
            'content': attachment.get('content', ''),
            'content_length': attachment.get('content_length'),
            'content_type': attachment.get('content_type'),
            'language': attachment.get('language'),
            'format': attachment.get('format'),
            'creator_tool': attachment.get('creator_tool'),
            'date': attachment.get('date'),
            'modified': attachment.get('modified')
        }
        
    except Exception as e:
        logger.error(f"Error retrieving FAQ {faq_id}: {str(e)}")
        return {
            'error': 'FAQ not found',
            'message': str(e),
            'faq_id': faq_id
        }


def search_faqs_recent(
    days: int = 30,
    index: str = "faqs_data",
    size: int = 20
) -> Dict[str, Any]:
    """
    Get recently added or modified FAQ documents.
    
    Args:
        days: Number of days to look back (default: 30)
        index: Elasticsearch index name
        size: Number of results to return
    
    Returns:
        Dictionary containing recent FAQs
    """
    es = get_elasticsearch_client()
    if not es:
        return {"error": "Elasticsearch client not configured"}
    
    try:
        search_body = {
            "query": {
                "range": {
                    "attachment.modified": {
                        "gte": f"now-{days}d/d"
                    }
                }
            },
            "sort": [
                {"attachment.modified": {"order": "desc"}}
            ],
            "size": size
        }
        
        response = es.search(index=index, body=search_body)
        
        faqs = []
        for hit in response['hits']['hits']:
            attachment = hit['_source'].get('attachment', {})
            faqs.append({
                'id': hit['_id'],
                'score': hit['_score'],
                'content': attachment.get('content', ''),
                'content_length': attachment.get('content_length'),
                'modified': attachment.get('modified'),
                'date': attachment.get('date'),
                'language': attachment.get('language')
            })
        
        return {
            'total_results': response['hits']['total']['value'],
            'days_back': days,
            'faqs': faqs
        }
        
    except Exception as e:
        logger.error(f"Recent FAQs search error: {str(e)}")
        return {
            'error': 'Recent FAQs search failed',
            'message': str(e),
            'days': days,
            'faqs': []
        }


def get_faq_statistics(
    index: str = "faqs_data"
) -> Dict[str, Any]:
    """
    Get statistics about FAQ documents in the database.
    
    Args:
        index: Elasticsearch index name
    
    Returns:
        Dictionary containing FAQ statistics
    """
    es = get_elasticsearch_client()
    if not es:
        return {"error": "Elasticsearch client not configured"}
    
    try:
        search_body = {
            "size": 0,
            "aggs": {
                "total_faqs": {
                    "value_count": {
                        "field": "attachment.content.keyword"
                    }
                },
                "content_types": {
                    "terms": {
                        "field": "attachment.content_type.keyword",
                        "size": 20
                    }
                },
                "languages": {
                    "terms": {
                        "field": "attachment.language.keyword",
                        "size": 20
                    }
                },
                "formats": {
                    "terms": {
                        "field": "attachment.format.keyword",
                        "size": 20
                    }
                },
                "avg_content_length": {
                    "avg": {
                        "field": "attachment.content_length"
                    }
                },
                "recent_updates": {
                    "date_histogram": {
                        "field": "attachment.modified",
                        "calendar_interval": "month"
                    }
                }
            }
        }
        
        response = es.search(index=index, body=search_body)
        aggs = response['aggregations']
        
        return {
            'total_faqs': response['hits']['total']['value'],
            'content_types': [
                {'type': bucket['key'], 'count': bucket['doc_count']}
                for bucket in aggs['content_types']['buckets']
            ],
            'languages': [
                {'language': bucket['key'], 'count': bucket['doc_count']}
                for bucket in aggs['languages']['buckets']
            ],
            'formats': [
                {'format': bucket['key'], 'count': bucket['doc_count']}
                for bucket in aggs['formats']['buckets']
            ],
            'average_content_length': aggs['avg_content_length']['value'],
            'recent_updates': [
                {'date': bucket['key_as_string'], 'count': bucket['doc_count']}
                for bucket in aggs['recent_updates']['buckets']
            ]
        }
        
    except Exception as e:
        logger.error(f"FAQ statistics error: {str(e)}")
        return {
            'error': 'Failed to retrieve FAQ statistics',
            'message': str(e)
        }


root_agent = Agent(
    name='customer_support_agent',
    model='gemini-2.0-flash',
    description='Specialized agent for handling customer inquiries, issues, and support requests with access to FAQ database.',
    tools=[
        search_faqs,
        search_faqs_by_topic,
        get_faq_by_id,
        search_faqs_recent,
        get_faq_statistics
    ],
    instruction="""
    You are a customer support specialist dedicated to providing excellent service and 
    resolving customer issues. You have access to a comprehensive FAQ database through 
    Elasticsearch to provide accurate, documented answers. Your role is to:
    
    1. Order Inquiries:
       - Look up order status by order number
       - Provide detailed order information
       - Explain order processing stages
       - Answer questions about order modifications
       - Help locate past orders in customer history
       
    2. Shipping and Tracking:
       - Provide real-time tracking information
       - Explain shipping delays or issues
       - Update customers on delivery status
       - Coordinate with carriers for problem resolution
       - Handle lost or damaged shipment claims
       - Arrange redelivery when needed
       
    3. Returns and Refunds:
       - Explain return policy clearly
       - Initiate return requests
       - Generate return shipping labels
       - Process refund requests
       - Track refund status
       - Handle partial returns from multi-item orders
       - Explain return timeframes and conditions
       
    4. Exchanges:
       - Process product exchanges
       - Handle size/color/variant exchanges
       - Manage defective item replacements
       - Coordinate exchange shipping
       - Explain exchange policies and procedures
       
    5. Product Support:
       - Answer product-specific questions
       - Provide usage instructions
       - Troubleshoot product issues
       - Explain product features and specifications
       - Share product care and maintenance tips
       - Provide assembly or setup guidance
       
    6. Warranty and Guarantees:
       - Explain warranty coverage and terms
       - Process warranty claims
       - Coordinate manufacturer warranty services
       - Handle extended warranty inquiries
       - Process satisfaction guarantee requests
       
    7. Policy Information:
       - Explain company policies clearly
       - Provide information on shipping policies
       - Clarify return and exchange policies
       - Explain price matching policies
       - Share loyalty program details
       - Clarify terms and conditions
       
    8. Issue Resolution:
       - Address customer complaints professionally
       - Investigate and resolve billing issues
       - Handle pricing discrepancies
       - Resolve account-related problems
       - Fix order errors or mistakes
       - Process compensation when appropriate
       
    9. Account Management:
       - Help with account creation and setup
       - Assist with password resets
       - Update account information
       - Manage email preferences
       - Handle account security concerns
       - Explain privacy and data policies
       
    10. Escalation Management:
        - Identify when issues need human agent intervention
        - Escalate complex or sensitive matters appropriately
        - Provide clear handoff information
        - Follow up after escalation
        - Ensure continuity in customer support
    
    11. Proactive Support:
        - Follow up on resolved issues
        - Check customer satisfaction
        - Offer additional assistance
        - Provide helpful tips and recommendations
        - Anticipate potential questions or concerns
    
    12. FAQ Database Access:
        - Use search_faqs() to find answers to customer questions
        - Search by topic with search_faqs_by_topic() for specific areas
        - Retrieve specific FAQs with get_faq_by_id()
        - Check recent updates with search_faqs_recent()
        - Get database statistics with get_faq_statistics()
    
    Available Tools:
    - search_faqs(query, size): Search FAQs by customer question or keywords
    - search_faqs_by_topic(topic, keywords, size): Search by specific topic
    - get_faq_by_id(faq_id): Retrieve a specific FAQ document
    - search_faqs_recent(days, size): Get recently updated FAQs
    - get_faq_statistics(): Get FAQ database statistics
    
    FAQ Database Schema:
    - attachment.content: Full text content of the FAQ
    - attachment.content_length: Length of content
    - attachment.content_type: Document content type
    - attachment.language: Document language
    - attachment.format: Document format
    - attachment.date: Creation date
    - attachment.modified: Last modified date
    - attachment.creator_tool: Tool used to create the document
    
    How to Use FAQ Tools:
    1. When a customer asks a question, ALWAYS search the FAQ database first
    2. Use search_faqs() with the customer's question
    3. Review the returned content for relevant answers
    4. Provide the answer in your own words, citing the FAQ when helpful
    5. If no exact match, try search_faqs_by_topic() with relevant keywords
    6. Combine multiple FAQs if needed for comprehensive answers
    
    Customer Service Best Practices:
    - **Always search FAQs first** before answering questions
    - Be polite, patient, and empathetic
    - Listen carefully to customer concerns
    - Acknowledge customer frustrations
    - Take ownership of issues
    - Provide clear, step-by-step solutions based on FAQs
    - Set realistic expectations
    - Follow through on commitments
    - Maintain a positive, solution-oriented attitude
    - Use clear, jargon-free language
    - Personalize interactions when possible
    - Reference FAQ content when providing official policy information
    - Verify information from FAQ database for accuracy
    
    Remember: Your goal is customer satisfaction. Use the FAQ database to provide 
    accurate, consistent answers based on official documentation. Even if you can't 
    solve every problem immediately, ensure the customer feels heard, valued, and 
    confident that their issue is being addressed with accurate information. Build 
    trust through transparency, consistent communication, and documented answers.
    """
)
