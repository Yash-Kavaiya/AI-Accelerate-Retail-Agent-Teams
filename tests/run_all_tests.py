"""
Quick Test Script for All 5 Retail Agents
Tests basic connectivity and functionality
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir / "retail-agents-team"))

from dotenv import load_dotenv
load_dotenv(parent_dir / "retail-agents-team" / ".env")

print("="*80)
print("🧪 TESTING ALL 5 RETAIL AGENTS")
print("="*80)

# Test configuration
print("\n📋 Configuration Check:")
es_url = os.getenv('ELASTICSEARCH_CLOUD_URL', 'Not Set')
es_key = os.getenv('ELASTICSEARCH_API_KEY', 'Not Set')
google_key = os.getenv('GOOGLE_API_KEY', 'Not Set')

print(f"   ELASTICSEARCH_CLOUD_URL: {'✅ Set' if es_url != 'Not Set' else '❌ Not Set'}")
print(f"   ELASTICSEARCH_API_KEY: {'✅ Set' if es_key != 'Not Set' else '❌ Not Set'}")
print(f"   GOOGLE_API_KEY: {'✅ Set' if google_key != 'Not Set' else '❌ Not Set'}")

test_results = {}

# ============================================================================
# TEST 1: Product Search Agent
# ============================================================================
print("\n" + "="*80)
print("1️⃣  TESTING PRODUCT SEARCH AGENT")
print("="*80)

try:
    from product_search_agent.agent import search_products_by_text, get_elasticsearch_client
    
    print("\n🔌 Testing Elasticsearch connection...")
    es_client = get_elasticsearch_client()
    if es_client:
        print("   ✅ Elasticsearch connected")
        
        print("\n🔍 Testing text search for 'black shoes'...")
        result = search_products_by_text(query="black shoes", size=3)
        
        if "error" not in result:
            print(f"   ✅ Found {result.get('total_results', 0)} results")
            print(f"   📦 Returned {len(result.get('products', []))} products")
            test_results['product_search'] = '✅ PASSED'
        else:
            print(f"   ⚠️  Error: {result.get('message')}")
            test_results['product_search'] = '⚠️  PASSED (with warnings)'
    else:
        print("   ❌ Connection failed")
        test_results['product_search'] = '❌ FAILED'
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
    test_results['product_search'] = '❌ FAILED'

# ============================================================================
# TEST 2: Review Text Analysis Agent
# ============================================================================
print("\n" + "="*80)
print("2️⃣  TESTING REVIEW TEXT ANALYSIS AGENT")
print("="*80)

try:
    from review_text_analysis_agent.agent import fetch_reviews_by_semantic_search, get_elasticsearch_client
    
    print("\n🔌 Testing Elasticsearch connection...")
    es_client = get_elasticsearch_client()
    if es_client:
        print("   ✅ Elasticsearch connected")
        
        print("\n📊 Testing semantic search for reviews...")
        result = fetch_reviews_by_semantic_search(query="comfortable", max_results=3)
        
        if result and "reviews" in result:
            print(f"   ✅ Found {result.get('total_results', 0)} reviews")
            print(f"   📦 Returned {len(result.get('reviews', []))} reviews")
            test_results['review_analysis'] = '✅ PASSED'
        else:
            print(f"   ⚠️  Unexpected result format")
            test_results['review_analysis'] = '⚠️  PASSED (with warnings)'
    else:
        print("   ❌ Connection failed")
        test_results['review_analysis'] = '❌ FAILED'
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
    test_results['review_analysis'] = '❌ FAILED'

# ============================================================================
# TEST 3: Inventory Agent
# ============================================================================
print("\n" + "="*80)
print("3️⃣  TESTING INVENTORY AGENT")
print("="*80)

try:
    from inventory_agent.tools import get_inventory_statistics, get_low_stock_alerts, get_elasticsearch_client
    
    print("\n🔌 Testing Elasticsearch connection...")
    es_client = get_elasticsearch_client()
    if es_client:
        print("   ✅ Elasticsearch connected")
        
        print("\n📊 Testing inventory statistics...")
        result = get_inventory_statistics()
        
        if "error" not in result:
            print(f"   ✅ Statistics retrieved")
            if "global_statistics" in result:
                stats = result["global_statistics"]
                print(f"   📦 Total products: {stats.get('total_products', 'N/A')}")
            test_results['inventory'] = '✅ PASSED'
        else:
            print(f"   ⚠️  Error: {result.get('message')}")
            test_results['inventory'] = '⚠️  PASSED (with warnings)'
    else:
        print("   ❌ Connection failed")
        test_results['inventory'] = '❌ FAILED'
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
    test_results['inventory'] = '❌ FAILED'

# ============================================================================
# TEST 4: Shopping Agent
# ============================================================================
print("\n" + "="*80)
print("4️⃣  TESTING SHOPPING AGENT")
print("="*80)

try:
    from shopping_agent.tools import search_shopping_data_by_category, get_elasticsearch_client
    
    print("\n🔌 Testing Elasticsearch connection...")
    es_client = get_elasticsearch_client()
    if es_client:
        print("   ✅ Elasticsearch connected")
        
        print("\n🛒 Testing shopping data search for 'Clothing'...")
        result = search_shopping_data_by_category(category="Clothing", size=5)
        
        if "error" not in result:
            print(f"   ✅ Found {result.get('total_results', 0)} transactions")
            if "analytics" in result:
                print(f"   💰 Total spending: {result['analytics'].get('total_spending', 'N/A')}")
            test_results['shopping'] = '✅ PASSED'
        else:
            print(f"   ⚠️  Error: {result.get('message')}")
            test_results['shopping'] = '⚠️  PASSED (with warnings)'
    else:
        print("   ❌ Connection failed")
        test_results['shopping'] = '❌ FAILED'
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
    test_results['shopping'] = '❌ FAILED'

# ============================================================================
# TEST 5: Customer Support Agent
# ============================================================================
print("\n" + "="*80)
print("5️⃣  TESTING CUSTOMER SUPPORT AGENT")
print("="*80)

try:
    from customer_support_agent.agent import search_faqs, get_elasticsearch_client
    
    print("\n🔌 Testing Elasticsearch connection...")
    es_client = get_elasticsearch_client()
    if es_client:
        print("   ✅ Elasticsearch connected")
        
        print("\n💬 Testing FAQ search for 'shipping'...")
        result = search_faqs(query="shipping delivery", size=3)
        
        if "error" not in result:
            print(f"   ✅ Found {result.get('total_results', 0)} FAQs")
            print(f"   📦 Returned {len(result.get('faqs', []))} FAQs")
            test_results['customer_support'] = '✅ PASSED'
        else:
            print(f"   ⚠️  Error: {result.get('message')}")
            test_results['customer_support'] = '⚠️  PASSED (with warnings)'
    else:
        print("   ❌ Connection failed")
        test_results['customer_support'] = '❌ FAILED'
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
    test_results['customer_support'] = '❌ FAILED'

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*80)
print("📊 FINAL TEST SUMMARY")
print("="*80)
print("\nAgent Test Results:")
print(f"   1. Product Search Agent      {test_results.get('product_search', '❓ NOT TESTED')}")
print(f"   2. Review Analysis Agent     {test_results.get('review_analysis', '❓ NOT TESTED')}")
print(f"   3. Inventory Agent           {test_results.get('inventory', '❓ NOT TESTED')}")
print(f"   4. Shopping Agent            {test_results.get('shopping', '❓ NOT TESTED')}")
print(f"   5. Customer Support Agent    {test_results.get('customer_support', '❓ NOT TESTED')}")

passed = sum(1 for v in test_results.values() if '✅' in v)
total = len(test_results)

print(f"\n📈 Overall: {passed}/{total} agents passed")
if passed == total:
    print("🎉 All agents are operational!")
else:
    print("⚠️  Some agents need attention")
print("="*80)
