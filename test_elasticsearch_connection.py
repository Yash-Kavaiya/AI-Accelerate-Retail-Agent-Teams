"""
Test Elasticsearch Connection
Quick script to verify Elasticsearch connection and configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("=" * 70)
print("🔍 Testing Elasticsearch Connection")
print("=" * 70)

# Check environment variables
print("\n📋 Environment Variables:")
cloud_id = os.getenv('ELASTICSEARCH_CLOUD_ID')
api_key = os.getenv('ELASTICSEARCH_API_KEY')

if cloud_id:
    # Mask the Cloud ID for security (show first/last 10 chars)
    masked_cloud_id = cloud_id[:15] + "..." + cloud_id[-10:] if len(cloud_id) > 30 else cloud_id
    print(f"   ✅ ELASTICSEARCH_CLOUD_ID: {masked_cloud_id}")
else:
    print(f"   ❌ ELASTICSEARCH_CLOUD_ID: Not set")

if api_key:
    # Mask the API key (show first/last 5 chars)
    masked_api_key = api_key[:8] + "..." + api_key[-8:] if len(api_key) > 20 else "***"
    print(f"   ✅ ELASTICSEARCH_API_KEY: {masked_api_key}")
else:
    print(f"   ❌ ELASTICSEARCH_API_KEY: Not set")

# Try to import and connect
print("\n🔌 Testing Connection:")
try:
    from elasticsearch import Elasticsearch
    print("   ✅ Elasticsearch package imported successfully")
    
    if cloud_id and api_key:
        # Create client
        es = Elasticsearch(
            cloud_id=cloud_id,
            api_key=api_key
        )
        
        # Test connection
        info = es.info()
        print(f"   ✅ Connected to Elasticsearch!")
        print(f"   📊 Cluster: {info['cluster_name']}")
        print(f"   🏷️  Version: {info['version']['number']}")
        print(f"   🆔 Cluster UUID: {info['cluster_uuid']}")
        
        # Test if products index exists
        print("\n📦 Checking Products Index:")
        try:
            if es.indices.exists(index='products'):
                count = es.count(index='products')
                print(f"   ✅ 'products' index exists")
                print(f"   📈 Total documents: {count['count']}")
            else:
                print(f"   ⚠️  'products' index does not exist")
                print(f"   💡 Create it with: PUT /products")
        except Exception as e:
            print(f"   ⚠️  Could not check index: {str(e)}")
        
        # Try a simple test search
        print("\n🔍 Testing Search:")
        try:
            result = es.search(index='products', body={"query": {"match_all": {}}, "size": 1})
            print(f"   ✅ Search successful!")
            if result['hits']['total']['value'] > 0:
                print(f"   📄 Sample product found:")
                product = result['hits']['hits'][0]['_source']
                print(f"      - Name: {product.get('name', 'N/A')}")
                print(f"      - Price: ${product.get('price', 'N/A')}")
            else:
                print(f"   ⚠️  No products found in index")
        except Exception as e:
            if 'index_not_found_exception' in str(e):
                print(f"   ⚠️  Index 'products' not found - need to create it first")
            else:
                print(f"   ⚠️  Search test failed: {str(e)}")
        
        print("\n" + "=" * 70)
        print("✅ SUCCESS! Elasticsearch is configured and working!")
        print("=" * 70)
        print("\n🚀 Next Steps:")
        print("   1. Create products index (if not exists)")
        print("   2. Load sample product data")
        print("   3. Run: adk web retail-agents-team/")
        print("\n")
        
    else:
        print("   ❌ Missing Cloud ID or API Key")
        print("   💡 Check your .env file configuration")
        
except ImportError:
    print("   ❌ Elasticsearch package not installed")
    print("   💡 Run: pip install elasticsearch")
except Exception as e:
    print(f"   ❌ Connection failed: {str(e)}")
    print("\n🔧 Troubleshooting:")
    print("   1. Verify Cloud ID and API Key are correct")
    print("   2. Check if Elasticsearch deployment is active")
    print("   3. Verify API Key has proper permissions")
    print("   4. Check network connectivity")
