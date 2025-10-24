"""
Direct test of FAQ search to verify it works with the agent
"""

import sys
from pathlib import Path

# Add retail-agents-team to path
sys.path.insert(0, str(Path(__file__).parent / "retail-agents-team"))

from customer_support_agent.agent import search_faqs

# Test the search function
print("\n" + "="*80)
print("Testing FAQ Search - Direct Call")
print("="*80 + "\n")

query = "return policy"
print(f"Searching for: '{query}'")
print()

result = search_faqs(query, size=2)

if 'error' in result:
    print(f"❌ Error: {result['error']}")
    print(f"   Message: {result.get('message', 'Unknown error')}")
else:
    print(f"✅ Found {result['total_results']} FAQs\n")
    
    for idx, faq in enumerate(result['faqs'], 1):
        print(f"FAQ {idx}:")
        print(f"  - ID: {faq.get('id', 'N/A')}")
        print(f"  - Score: {faq.get('score', 'N/A')}")
        print(f"  - Content Length: {faq.get('content_length', 'N/A')} chars")
        print(f"  - Language: {faq.get('language', 'N/A')}")
        
        # Show first 200 characters
        content = faq.get('content', '')
        preview = content[:200] + "..." if len(content) > 200 else content
        print(f"  - Preview:\n    {preview}")
        print()

print("="*80)
print("✅ Direct FAQ search test completed!")
print("="*80)
