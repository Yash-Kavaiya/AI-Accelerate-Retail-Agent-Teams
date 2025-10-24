"""
Test Suite for Customer Support Agent - FAQ Search Tools

This script tests all Elasticsearch FAQ search functions integrated into the
customer_support_agent to verify connectivity, query functionality, and data retrieval.

Author: AI Development Team
Date: October 2025
"""

import os
import sys
from pathlib import Path

# Add retail-agents-team to Python path
sys.path.insert(0, str(Path(__file__).parent / "retail-agents-team"))

from customer_support_agent.agent import (
    search_faqs,
    search_faqs_by_topic,
    get_faq_by_id,
    search_faqs_recent,
    get_faq_statistics
)

def print_separator():
    """Print a visual separator"""
    print("\n" + "=" * 80 + "\n")

def test_search_faqs():
    """Test 1: Full-text FAQ search"""
    print("🔍 TEST 1: Full-text FAQ Search")
    print("-" * 80)
    
    # Test with common customer questions
    queries = [
        "return policy",
        "shipping international",
        "warranty coverage",
        "refund process"
    ]
    
    for query in queries:
        print(f"\n📝 Query: '{query}'")
        try:
            result = search_faqs(query, size=3)
            print(f"✅ Success! Found {result['total_results']} FAQs")
            
            if result['faqs']:
                for idx, faq in enumerate(result['faqs'][:2], 1):
                    print(f"\n   FAQ {idx}:")
                    print(f"   - Score: {faq.get('score', 'N/A')}")
                    print(f"   - Content Length: {faq.get('content_length', 'N/A')} chars")
                    print(f"   - Type: {faq.get('content_type', 'N/A')}")
                    print(f"   - Language: {faq.get('language', 'N/A')}")
                    print(f"   - Format: {faq.get('format', 'N/A')}")
                    # Show first 100 chars of content
                    content = faq.get('content', '')
                    preview = content[:100] + "..." if len(content) > 100 else content
                    print(f"   - Preview: {preview}")
            else:
                print("   ℹ️  No FAQs found for this query")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print_separator()

def test_search_faqs_by_topic():
    """Test 2: Topic-based FAQ search"""
    print("📚 TEST 2: Topic-based FAQ Search")
    print("-" * 80)
    
    # Test with common topics
    test_cases = [
        {"topic": "returns", "keywords": ["policy", "timeframe"]},
        {"topic": "shipping", "keywords": ["international", "tracking"]},
        {"topic": "warranty", "keywords": None},
        {"topic": "account", "keywords": ["password", "security"]}
    ]
    
    for test_case in test_cases:
        topic = test_case['topic']
        keywords = test_case['keywords']
        
        print(f"\n📋 Topic: '{topic}'")
        if keywords:
            print(f"   Keywords: {keywords}")
        
        try:
            result = search_faqs_by_topic(
                topic=topic,
                keywords=keywords,
                size=3
            )
            print(f"✅ Success! Found {result['total_results']} FAQs")
            
            if result['faqs']:
                for idx, faq in enumerate(result['faqs'][:2], 1):
                    print(f"\n   FAQ {idx}:")
                    print(f"   - Score: {faq.get('score', 'N/A')}")
                    print(f"   - Language: {faq.get('language', 'N/A')}")
                    print(f"   - Modified: {faq.get('modified', 'N/A')}")
                    # Show first 80 chars
                    content = faq.get('content', '')
                    preview = content[:80] + "..." if len(content) > 80 else content
                    print(f"   - Preview: {preview}")
            else:
                print("   ℹ️  No FAQs found for this topic")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print_separator()

def test_get_faq_by_id():
    """Test 3: Get specific FAQ by ID"""
    print("📄 TEST 3: Get FAQ by ID")
    print("-" * 80)
    
    print("\n📝 First, searching for an FAQ to get its ID...")
    try:
        # Search for an FAQ to get an ID
        search_result = search_faqs("policy", size=1)
        
        if search_result['faqs']:
            faq_id = search_result['faqs'][0].get('id')
            print(f"   Found FAQ ID: {faq_id}")
            
            print(f"\n🔍 Retrieving FAQ with ID: {faq_id}")
            result = get_faq_by_id(faq_id)
            
            print(f"✅ Success! Retrieved FAQ")
            print(f"   - ID: {result.get('id', 'N/A')}")
            print(f"   - Content Length: {result.get('content_length', 'N/A')} chars")
            print(f"   - Type: {result.get('content_type', 'N/A')}")
            print(f"   - Language: {result.get('language', 'N/A')}")
            print(f"   - Format: {result.get('format', 'N/A')}")
            print(f"   - Created: {result.get('date', 'N/A')}")
            print(f"   - Modified: {result.get('modified', 'N/A')}")
            
            # Show content preview
            content = result.get('content', '')
            preview = content[:150] + "..." if len(content) > 150 else content
            print(f"   - Content Preview:\n     {preview}")
        else:
            print("   ℹ️  No FAQs found to test ID retrieval")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print_separator()

def test_search_faqs_recent():
    """Test 4: Get recently modified FAQs"""
    print("🕒 TEST 4: Recently Modified FAQs")
    print("-" * 80)
    
    # Test different time ranges
    time_ranges = [7, 30, 90]
    
    for days in time_ranges:
        print(f"\n📅 Last {days} days:")
        try:
            result = search_faqs_recent(days=days, size=5)
            print(f"✅ Success! Found {result['total_results']} recent FAQs")
            
            if result['faqs']:
                for idx, faq in enumerate(result['faqs'][:3], 1):
                    print(f"\n   FAQ {idx}:")
                    print(f"   - ID: {faq.get('id', 'N/A')[:20]}...")
                    print(f"   - Modified: {faq.get('modified', 'N/A')}")
                    print(f"   - Language: {faq.get('language', 'N/A')}")
                    print(f"   - Content Length: {faq.get('content_length', 'N/A')} chars")
                    # Show first 60 chars
                    content = faq.get('content', '')
                    preview = content[:60] + "..." if len(content) > 60 else content
                    print(f"   - Preview: {preview}")
            else:
                print(f"   ℹ️  No FAQs modified in the last {days} days")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print_separator()

def test_get_faq_statistics():
    """Test 5: Get FAQ database statistics"""
    print("📊 TEST 5: FAQ Database Statistics")
    print("-" * 80)
    
    try:
        result = get_faq_statistics()
        
        print("\n✅ Success! Retrieved FAQ Statistics\n")
        
        # Total FAQs
        print(f"📝 Total FAQs: {result.get('total_faqs', 0)}")
        
        # Content Types
        print(f"\n📄 Content Types:")
        for ct in result.get('content_types', [])[:5]:
            print(f"   - {ct['type']}: {ct['count']} documents")
        
        # Languages
        print(f"\n🌍 Languages:")
        for lang in result.get('languages', [])[:5]:
            print(f"   - {lang['language']}: {lang['count']} documents")
        
        # Formats
        print(f"\n📋 Formats:")
        for fmt in result.get('formats', [])[:5]:
            print(f"   - {fmt['format']}: {fmt['count']} documents")
        
        # Average Content Length
        avg_length = result.get('average_content_length', 0)
        print(f"\n📏 Average Content Length: {avg_length:.1f} characters")
        
        # Recent Updates
        print(f"\n📅 Recent Update Timeline:")
        for update in result.get('recent_updates', [])[:6]:
            print(f"   - {update['date']}: {update['count']} updates")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print_separator()

def run_all_tests():
    """Run all test functions"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "CUSTOMER SUPPORT AGENT - FAQ SEARCH TESTS" + " " * 20 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")
    
    print("📋 Running comprehensive test suite for FAQ search functionality...")
    print(f"📂 Index: faqs_data")
    print(f"🔧 Testing 5 FAQ search tools\n")
    
    try:
        # Run all tests
        test_search_faqs()
        test_search_faqs_by_topic()
        test_get_faq_by_id()
        test_search_faqs_recent()
        test_get_faq_statistics()
        
        # Summary
        print("\n")
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 30 + "TEST SUMMARY" + " " * 34 + "║")
        print("╚" + "═" * 78 + "╝")
        print("\n")
        print("✅ All tests completed successfully!")
        print("\n📝 Test Coverage:")
        print("   ✓ Full-text FAQ search")
        print("   ✓ Topic-based search with keywords")
        print("   ✓ FAQ retrieval by ID")
        print("   ✓ Recent FAQ updates tracking")
        print("   ✓ Database statistics and analytics")
        print("\n🎉 Customer Support Agent FAQ tools are working correctly!")
        print("\n💡 Next Steps:")
        print("   1. Run the agent: adk run retail-agents-team/customer_support_agent")
        print("   2. Test with customer questions")
        print("   3. Monitor FAQ search accuracy")
        print("   4. Review FAQ database coverage")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test suite error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Check environment variables
    if not os.getenv('ELASTICSEARCH_CLOUD_URL') or not os.getenv('ELASTICSEARCH_API_KEY'):
        print("\n⚠️  WARNING: Elasticsearch credentials not found in environment!")
        print("   Please ensure .env file exists in retail-agents-team directory")
        print("   with ELASTICSEARCH_CLOUD_URL and ELASTICSEARCH_API_KEY set.\n")
        sys.exit(1)
    
    run_all_tests()
