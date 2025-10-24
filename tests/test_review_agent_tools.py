"""
Test script for Review Text Analysis Agent Elasticsearch tools
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the retail-agents-team to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'retail-agents-team', 'review_text_analysis_agent'))

from agent import (
    fetch_reviews_by_semantic_search,
    fetch_reviews_by_rating,
    aggregate_rating_statistics,
    fetch_reviews_by_department,
    fetch_reviews_by_class
)


def test_semantic_search():
    """Test semantic search functionality"""
    print("\n" + "="*80)
    print("TEST 1: Semantic Search for 'comfortable fabric'")
    print("="*80)
    
    result = fetch_reviews_by_semantic_search("comfortable fabric", max_results=3)
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        return False
    
    print(f"✅ Found {result['total_results']} total results")
    print(f"\nShowing {len(result['reviews'])} reviews:")
    
    for i, review in enumerate(result['reviews'], 1):
        print(f"\n--- Review {i} ---")
        print(f"Score: {review['score']}")
        print(f"Rating: {review['rating']}/5")
        print(f"Title: {review['title']}")
        print(f"Review: {review['review_text'][:150]}...")
        print(f"Department: {review['department_name']}")
        print(f"Class: {review['class_name']}")
        print(f"Alike Feedback: {review['alike_feedback_count']}")
    
    return True


def test_rating_filter():
    """Test rating filter functionality"""
    print("\n" + "="*80)
    print("TEST 2: Filter Reviews by Rating (5 stars only)")
    print("="*80)
    
    result = fetch_reviews_by_rating(min_rating=5, max_rating=5, max_results=3)
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        return False
    
    print(f"✅ Found {result['total_results']} total 5-star reviews")
    print(f"\nShowing {len(result['reviews'])} reviews:")
    
    for i, review in enumerate(result['reviews'], 1):
        print(f"\n--- Review {i} ---")
        print(f"Rating: {review['rating']}/5")
        print(f"Title: {review['title']}")
        print(f"Department: {review['department_name']}")
        print(f"Class: {review['class_name']}")
    
    return True


def test_aggregate_statistics():
    """Test aggregate statistics functionality"""
    print("\n" + "="*80)
    print("TEST 3: Aggregate Rating Statistics")
    print("="*80)
    
    result = aggregate_rating_statistics()
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        return False
    
    print(f"✅ Statistics retrieved successfully")
    print(f"\nOverall Statistics:")
    print(f"  Total Reviews: {result['total_reviews']}")
    print(f"  Average Rating: {result['average_rating']:.2f}/5")
    print(f"  Average Customer Age: {result['average_age']:.1f}")
    print(f"  Total Alike Feedback: {result['total_alike_feedback']}")
    
    print(f"\nRating Distribution:")
    for rating in sorted(result['rating_distribution'].keys(), reverse=True):
        count = result['rating_distribution'][rating]
        percentage = (count / result['total_reviews']) * 100
        print(f"  {rating} stars: {count} reviews ({percentage:.1f}%)")
    
    print(f"\nTop Departments:")
    for dept, count in list(result['department_distribution'].items())[:5]:
        print(f"  {dept}: {count} reviews")
    
    print(f"\nTop Product Classes:")
    for cls, count in list(result['class_distribution'].items())[:5]:
        print(f"  {cls}: {count} reviews")
    
    return True


def test_department_filter():
    """Test department filter functionality"""
    print("\n" + "="*80)
    print("TEST 4: Filter Reviews by Department")
    print("="*80)
    
    # First get available departments
    stats = aggregate_rating_statistics()
    if 'error' not in stats and stats['department_distribution']:
        department = list(stats['department_distribution'].keys())[0]
        print(f"Testing with department: {department}")
        
        result = fetch_reviews_by_department(department, max_results=3)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return False
        
        print(f"✅ Found {result['total_results']} reviews for {department}")
        print(f"\nShowing {len(result['reviews'])} reviews:")
        
        for i, review in enumerate(result['reviews'], 1):
            print(f"\n--- Review {i} ---")
            print(f"Rating: {review['rating']}/5")
            print(f"Title: {review['title']}")
            print(f"Class: {review['class_name']}")
        
        return True
    else:
        print("❌ Could not retrieve department list")
        return False


def test_class_filter():
    """Test class filter functionality"""
    print("\n" + "="*80)
    print("TEST 5: Filter Reviews by Product Class")
    print("="*80)
    
    # First get available classes
    stats = aggregate_rating_statistics()
    if 'error' not in stats and stats['class_distribution']:
        class_name = list(stats['class_distribution'].keys())[0]
        print(f"Testing with class: {class_name}")
        
        result = fetch_reviews_by_class(class_name, max_results=3)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return False
        
        print(f"✅ Found {result['total_results']} reviews for {class_name}")
        print(f"\nShowing {len(result['reviews'])} reviews:")
        
        for i, review in enumerate(result['reviews'], 1):
            print(f"\n--- Review {i} ---")
            print(f"Rating: {review['rating']}/5")
            print(f"Title: {review['title']}")
            print(f"Department: {review['department_name']}")
        
        return True
    else:
        print("❌ Could not retrieve class list")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("REVIEW TEXT ANALYSIS AGENT - ELASTICSEARCH TOOLS TEST")
    print("="*80)
    
    # Check environment variables
    es_url = os.getenv("ELASTICSEARCH_CLOUD_URL")
    es_key = os.getenv("ELASTICSEARCH_API_KEY")
    
    if not es_url or not es_key:
        print("\n⚠️  Warning: Elasticsearch credentials not found in environment variables")
        print("Using default values from code")
    else:
        print(f"\n✅ Elasticsearch URL configured: {es_url[:50]}...")
        print(f"✅ API Key configured: {es_key[:20]}...")
    
    # Run tests
    results = []
    
    results.append(("Semantic Search", test_semantic_search()))
    results.append(("Rating Filter", test_rating_filter()))
    results.append(("Aggregate Statistics", test_aggregate_statistics()))
    results.append(("Department Filter", test_department_filter()))
    results.append(("Class Filter", test_class_filter()))
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
    
    if total_passed == len(results):
        print("\n🎉 All tests passed! The agent is ready to use.")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")


if __name__ == "__main__":
    main()
