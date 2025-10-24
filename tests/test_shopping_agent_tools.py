"""
Test Shopping Agent Tools
Tests all Elasticsearch-based shopping data analysis functions.
"""

import sys
import os

# Add the retail-agents-team directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
retail_agents_dir = os.path.join(current_dir, 'retail-agents-team')
sys.path.insert(0, retail_agents_dir)

from shopping_agent.tools import (
    search_shopping_data_by_category,
    get_customer_purchase_history,
    analyze_shopping_trends_by_gender,
    get_high_value_transactions,
    analyze_shopping_mall_performance,
    get_payment_method_analytics,
    search_transactions_by_date_range
)

def test_search_by_category():
    """Test searching shopping data by category"""
    print("\n" + "="*80)
    print("TEST 1: Search Shopping Data by Category - 'Clothing'")
    print("="*80)
    
    result = search_shopping_data_by_category(
        category="Clothing",
        size=10
    )
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        print(f"   Message: {result['message']}")
    else:
        print(f"✅ Found {result['total_results']} transactions in category '{result['category']}'")
        print(f"\n📊 Analytics:")
        print(f"   Total Spending: ${result['analytics']['total_spending']}")
        print(f"   Average Price: ${result['analytics']['average_price']}")
        print(f"   Total Quantity: {result['analytics']['total_quantity']}")
        print(f"   Unique Malls: {result['analytics']['unique_malls']}")
        print(f"   Shopping Malls: {', '.join(result['analytics']['malls'][:3])}")
        print(f"   Payment Methods: {', '.join(result['analytics']['payment_methods'])}")
        print(f"   Gender Distribution: {result['analytics']['gender_distribution']}")
        
        if result['transactions']:
            print(f"\n📝 Sample Transactions (showing {len(result['transactions'])}):")
            for i, txn in enumerate(result['transactions'][:3], 1):
                print(f"   {i}. Invoice: {txn['invoice_no']} | "
                      f"Customer: {txn['customer_id']} | "
                      f"Qty: {txn['quantity']} | "
                      f"Price: ${txn['price']} | "
                      f"Mall: {txn['shopping_mall']}")


def test_customer_purchase_history():
    """Test getting customer purchase history"""
    print("\n" + "="*80)
    print("TEST 2: Get Customer Purchase History")
    print("="*80)
    
    # First, get a customer ID from a search
    search_result = search_shopping_data_by_category("Clothing", size=1)
    
    if "error" not in search_result and search_result['transactions']:
        customer_id = search_result['transactions'][0]['customer_id']
        
        result = get_customer_purchase_history(
            customer_id=customer_id,
            size=20
        )
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Customer ID: {result['customer_id']}")
            print(f"   Total Purchases: {result['total_purchases']}")
            
            profile = result['customer_profile']
            print(f"\n👤 Customer Profile:")
            print(f"   Gender: {profile['gender']}")
            print(f"   Age: {profile['age']}")
            
            spending = result['spending_analytics']
            print(f"\n💰 Spending Analytics:")
            print(f"   Total Spent: ${spending['total_spent']}")
            print(f"   Average Transaction: ${spending['average_transaction']}")
            print(f"   Total Items Purchased: {spending['total_items_purchased']}")
            print(f"   Avg Items per Transaction: {spending['average_items_per_transaction']}")
            
            prefs = result['preferences']
            print(f"\n🎯 Preferences:")
            print(f"   Favorite Categories: {prefs['favorite_categories'][:3]}")
            print(f"   Favorite Malls: {prefs['favorite_malls'][:3]}")
            print(f"   Payment Methods: {prefs['payment_methods']}")
            
            if result['purchase_history']:
                print(f"\n📝 Recent Purchases (showing 3):")
                for i, purchase in enumerate(result['purchase_history'][:3], 1):
                    print(f"   {i}. {purchase['date']} | "
                          f"{purchase['category']} | "
                          f"Qty: {purchase['quantity']} | "
                          f"Total: ${purchase['total']}")
    else:
        print("⚠️ Could not find a customer ID to test with")


def test_gender_analysis():
    """Test analyzing shopping trends by gender"""
    print("\n" + "="*80)
    print("TEST 3: Analyze Shopping Trends by Gender - 'Female'")
    print("="*80)
    
    result = analyze_shopping_trends_by_gender(
        gender="Female",
        size=100
    )
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print(f"✅ Gender: {result['gender']}")
        print(f"   Total Transactions: {result['total_transactions']}")
        print(f"   Sample Size: {result['sample_size']}")
        
        demo = result['demographics']
        print(f"\n👥 Demographics:")
        print(f"   Average Age: {demo['average_age']}")
        
        spending = result['spending_patterns']
        print(f"\n💰 Spending Patterns:")
        print(f"   Average Price: ${spending['average_price']}")
        print(f"   Total Spending: ${spending['total_spending']}")
        
        print(f"\n🛍️ Top Category Preferences:")
        for i, cat in enumerate(result['category_preferences'][:5], 1):
            print(f"   {i}. {cat['category']}: {cat['purchase_count']} purchases, "
                  f"Avg: ${cat['avg_price']}, Qty: {cat['total_quantity']}")
        
        print(f"\n💳 Payment Preferences:")
        for i, pm in enumerate(result['payment_preferences'], 1):
            print(f"   {i}. {pm['payment_method']}: {pm['usage_count']} uses")
        
        print(f"\n🏬 Shopping Mall Preferences:")
        for i, mall in enumerate(result['shopping_mall_preferences'][:3], 1):
            print(f"   {i}. {mall['mall']}: {mall['visit_count']} visits")


def test_high_value_transactions():
    """Test getting high-value transactions"""
    print("\n" + "="*80)
    print("TEST 4: Get High-Value Transactions (>= $100)")
    print("="*80)
    
    result = get_high_value_transactions(
        min_amount=100.0,
        size=10
    )
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print(f"✅ Threshold: ${result['threshold']}")
        print(f"   Total Matching: {result['total_matching']}")
        print(f"   Transactions Shown: {result['transactions_shown']}")
        
        analytics = result['analytics']
        print(f"\n📊 Analytics:")
        print(f"   Total Value: ${analytics['total_value']}")
        print(f"   Average Value: ${analytics['average_value']}")
        print(f"   Highest Transaction: ${analytics['highest_transaction']}")
        
        if result['transactions']:
            print(f"\n💎 Top High-Value Transactions (showing 5):")
            for i, txn in enumerate(result['transactions'][:5], 1):
                print(f"   {i}. Invoice: {txn['invoice_no']} | "
                      f"${txn['total_amount']:.2f} | "
                      f"{txn['category']} | "
                      f"Qty: {txn['quantity']} × ${txn['unit_price']} | "
                      f"{txn['payment_method']}")


def test_mall_performance():
    """Test analyzing shopping mall performance"""
    print("\n" + "="*80)
    print("TEST 5: Analyze Shopping Mall Performance (All Malls)")
    print("="*80)
    
    result = analyze_shopping_mall_performance(
        shopping_mall=None,
        size=50
    )
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print(f"✅ Analysis Type: {result['analysis_type']}")
        print(f"   Total Malls Analyzed: {result['total_malls_analyzed']}")
        
        summary = result['summary']
        print(f"\n📊 Summary:")
        print(f"   Highest Revenue Mall: {summary['highest_revenue_mall']}")
        print(f"   Total Combined Revenue: ${summary['total_combined_revenue']}")
        print(f"   Total Transactions: {summary['total_transactions']}")
        
        print(f"\n🏬 Mall Performance (Top 3):")
        for i, mall in enumerate(result['mall_performance'][:3], 1):
            print(f"\n   {i}. {mall['mall_name']}")
            print(f"      Transactions: {mall['total_transactions']}")
            print(f"      Revenue: ${mall['total_revenue']}")
            print(f"      Avg Transaction: ${mall['average_transaction_value']}")
            print(f"      Avg Customer Age: {mall['average_customer_age']}")
            print(f"      Top Categories: {', '.join([c['category'] for c in mall['top_categories'][:3]])}")


def test_payment_analytics():
    """Test payment method analytics"""
    print("\n" + "="*80)
    print("TEST 6: Payment Method Analytics")
    print("="*80)
    
    result = get_payment_method_analytics(size=100)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print(f"✅ Total Transactions: {result['total_transactions_analyzed']}")
        print(f"   Total Revenue: ${result['total_revenue']}")
        print(f"   Payment Methods: {result['payment_methods_count']}")
        print(f"   Most Popular: {result['most_popular_method']}")
        print(f"   Highest Revenue: {result['highest_revenue_method']}")
        
        print(f"\n💳 Payment Method Breakdown:")
        for i, pm in enumerate(result['payment_method_analytics'], 1):
            print(f"\n   {i}. {pm['payment_method']}")
            print(f"      Usage: {pm['transaction_count']} ({pm['usage_percentage']}%)")
            print(f"      Revenue: ${pm['total_revenue']} ({pm['revenue_percentage']}%)")
            print(f"      Avg Transaction: ${pm['average_transaction_value']}")
            
            gender_info = ', '.join([f"{g['gender']}({g['count']})" for g in pm['gender_distribution']])
            print(f"      Gender: {gender_info}")
            
            age_stats = pm['customer_age_stats']
            print(f"      Customer Age: Avg {age_stats['average']}, "
                  f"Range {age_stats['min']}-{age_stats['max']}")


def test_date_range_search():
    """Test searching transactions by date range"""
    print("\n" + "="*80)
    print("TEST 7: Search Transactions by Date Range")
    print("="*80)
    
    result = search_transactions_by_date_range(
        start_date="2021-01-01",
        end_date="2021-12-31",
        size=20
    )
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        date_range = result['date_range']
        print(f"✅ Date Range: {date_range['start']} to {date_range['end']}")
        print(f"   Total Transactions: {result['total_transactions']}")
        print(f"   Transactions Shown: {result['transactions_shown']}")
        
        analytics = result['analytics']
        print(f"\n📊 Analytics:")
        print(f"   Total Revenue: ${analytics['total_revenue']}")
        print(f"   Average Transaction: ${analytics['average_transaction']}")
        
        print(f"\n🏆 Top Categories:")
        for i, cat in enumerate(analytics['top_categories'][:5], 1):
            print(f"   {i}. {cat['category']}: {cat['count']} transactions")
        
        if analytics['daily_sales']:
            print(f"\n📅 Daily Sales Sample (showing 5 days):")
            for i, day in enumerate(analytics['daily_sales'][:5], 1):
                print(f"   {i}. {day['date']}: {day['transaction_count']} transactions, ${day['revenue']}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🛍️  SHOPPING AGENT TOOLS TEST SUITE")
    print("="*80)
    
    try:
        test_search_by_category()
        test_customer_purchase_history()
        test_gender_analysis()
        test_high_value_transactions()
        test_mall_performance()
        test_payment_analytics()
        test_date_range_search()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*80)
        
    except Exception as e:
        print("\n" + "="*80)
        print(f"❌ TEST SUITE FAILED")
        print("="*80)
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
