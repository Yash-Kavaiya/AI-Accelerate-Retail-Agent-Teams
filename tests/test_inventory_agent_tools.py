"""
Test script for Inventory Agent Tools
Tests all inventory management functions with the retail_store_inventory index.
"""

import sys
import os
from pathlib import Path
import importlib.util

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load the inventory tools module directly from file
inventory_tools_path = project_root / "retail-agents-team" / "inventory_agent" / "tools.py"
spec = importlib.util.spec_from_file_location("inventory_tools", inventory_tools_path)
inventory_tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory_tools)

# Import functions from the module
check_product_inventory = inventory_tools.check_product_inventory
search_inventory_by_category = inventory_tools.search_inventory_by_category
get_low_stock_alerts = inventory_tools.get_low_stock_alerts
get_inventory_by_region = inventory_tools.get_inventory_by_region
check_demand_forecast = inventory_tools.check_demand_forecast
get_seasonal_inventory_analysis = inventory_tools.get_seasonal_inventory_analysis
get_inventory_statistics = inventory_tools.get_inventory_statistics
get_elasticsearch_client = inventory_tools.get_elasticsearch_client

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def test_elasticsearch_connection():
    """Test Elasticsearch connection."""
    print_section("Testing Elasticsearch Connection")
    
    client = get_elasticsearch_client()
    if client:
        try:
            info = client.info()
            print(f"✓ Connected to Elasticsearch cluster: {info['cluster_name']}")
            print(f"  Version: {info['version']['number']}")
            return True
        except Exception as e:
            print(f"✗ Connection failed: {str(e)}")
            return False
    else:
        print("✗ Failed to create Elasticsearch client")
        return False

def test_inventory_statistics():
    """Test getting overall inventory statistics."""
    print_section("Test 1: Get Inventory Statistics")
    
    result = get_inventory_statistics()
    
    if "error" in result:
        print(f"✗ Error: {result['error']} - {result['message']}")
        return
    
    print("✓ Successfully retrieved inventory statistics")
    print(f"\nTotal Products: {result['total_products']}")
    print(f"Total Inventory: {result['total_inventory']}")
    print(f"Total Units Sold: {result['total_units_sold']}")
    print(f"Unique Stores: {result['unique_stores']}")
    print(f"Average Inventory per Product: {result['average_inventory_per_product']}")
    print(f"Average Price: ${result['average_price']:.2f}")
    print(f"Low Stock Products: {result['low_stock_products']}")
    print(f"Out of Stock Products: {result['out_of_stock_products']}")
    
    print("\nTop Categories:")
    for cat in result['categories'][:5]:
        print(f"  - {cat['category']}: {cat['product_count']} products")
    
    print("\nRegions:")
    for region in result['regions']:
        print(f"  - {region['region']}: {region['product_count']} products")

def test_check_product_inventory():
    """Test checking inventory for a specific product."""
    print_section("Test 2: Check Product Inventory")
    
    # First, let's get a product ID from the statistics
    stats = get_inventory_statistics()
    if "error" in stats or stats['total_products'] == 0:
        print("✗ No products found in inventory")
        return
    
    # Try to get inventory by category first to find a product ID
    print("Fetching sample product ID...")
    category_result = search_inventory_by_category(
        category="Electronics",  # Try common category
        size=1
    )
    
    if "error" not in category_result and category_result.get('products'):
        product_id = category_result['products'][0]['product_id']
        print(f"Testing with Product ID: {product_id}")
        
        result = check_product_inventory(product_id=product_id)
        
        if "error" in result:
            print(f"✗ Error: {result['error']}")
        else:
            print(f"✓ Product ID: {result['product_id']}")
            print(f"  Stock Status: {result['stock_status']}")
            print(f"  Total Inventory: {result['total_inventory']}")
            print(f"  Locations: {result['location_count']}")
            
            if result['locations']:
                print("\n  Location Details:")
                for loc in result['locations'][:3]:
                    print(f"    Store {loc['store_id']} ({loc['region']}): {loc['inventory_level']} units")
    else:
        print("✗ Could not find sample product ID")

def test_search_by_category():
    """Test searching inventory by category."""
    print_section("Test 3: Search Inventory by Category")
    
    categories_to_test = ["Electronics", "Clothing", "Food"]
    
    for category in categories_to_test:
        print(f"\nSearching for '{category}'...")
        result = search_inventory_by_category(
            category=category,
            size=5
        )
        
        if "error" in result:
            print(f"  ✗ Error: {result['error']}")
        elif result['total_results'] == 0:
            print(f"  ℹ No results found for '{category}'")
        else:
            print(f"  ✓ Found {result['total_results']} products")
            print(f"    Total Inventory: {result['total_inventory']} units")
            print(f"    Sample Products: {len(result['products'])}")
            
            if result['products']:
                prod = result['products'][0]
                print(f"    Example: Product {prod['product_id']} - {prod['inventory_level']} units in stock")

def test_low_stock_alerts():
    """Test getting low stock alerts."""
    print_section("Test 4: Low Stock Alerts")
    
    result = get_low_stock_alerts(threshold=10, size=10)
    
    if "error" in result:
        print(f"✗ Error: {result['error']}")
    else:
        print(f"✓ Total Alerts: {result['total_alerts']}")
        print(f"  Critical Alerts (Out of Stock): {result['critical_alerts']}")
        print(f"  Low Stock Alerts: {result['low_stock_alerts']}")
        print(f"  Threshold: {result['threshold']} units")
        
        if result['alerts']:
            print("\n  Top Critical Products:")
            for alert in result['alerts'][:5]:
                print(f"    [{alert['severity'].upper()}] Product {alert['product_id']} - "
                      f"{alert['inventory_level']} units (Store: {alert['store_id']}, "
                      f"Region: {alert['region']})")

def test_regional_inventory():
    """Test getting regional inventory."""
    print_section("Test 5: Regional Inventory")
    
    regions = ["North", "South", "East", "West"]
    
    for region in regions:
        print(f"\nQuerying {region} region...")
        result = get_inventory_by_region(region=region, size=5)
        
        if "error" in result:
            print(f"  ✗ Error: {result['error']}")
        elif result['total_results'] == 0:
            print(f"  ℹ No data for {region} region")
        else:
            print(f"  ✓ Total Inventory: {result['total_inventory']} units")
            print(f"    Units Sold: {result['total_units_sold']}")
            print(f"    Stores: {result['store_count']}")
            print(f"    Categories: {len(result['categories'])}")
            break  # Just test one region that has data

def test_demand_forecast():
    """Test checking demand forecasts."""
    print_section("Test 6: Demand Forecast Analysis")
    
    # Get a sample category
    stats = get_inventory_statistics()
    if "error" not in stats and stats.get('categories'):
        category = stats['categories'][0]['category']
        print(f"Testing demand forecast for category: {category}")
        
        result = check_demand_forecast(category=category, size=5)
        
        if "error" in result:
            print(f"✗ Error: {result['error']}")
        else:
            print(f"✓ Total Products Analyzed: {result['total_products']}")
            print(f"  Products Needing Restock: {result['restock_required']}")
            
            if result['restock_recommendations']:
                print("\n  Restock Recommendations:")
                for rec in result['restock_recommendations'][:3]:
                    print(f"    Product {rec['product_id']}: Need {rec['shortage']} more units")
                    print(f"      Current: {rec['current_inventory']}, Forecast: {rec['demand_forecast']}")

def test_seasonal_analysis():
    """Test seasonal inventory analysis."""
    print_section("Test 7: Seasonal Inventory Analysis")
    
    seasons = ["Summer", "Winter", "Spring", "Fall"]
    
    for season in seasons:
        print(f"\nAnalyzing {season} inventory...")
        result = get_seasonal_inventory_analysis(seasonality=season, size=5)
        
        if "error" in result:
            print(f"  ✗ Error: {result['error']}")
        elif result['total_results'] == 0:
            print(f"  ℹ No {season} products found")
        else:
            print(f"  ✓ Total Inventory: {result['total_inventory']} units")
            print(f"    Demand Forecast: {result['total_demand_forecast']} units")
            print(f"    Readiness Score: {result['readiness_score']}%")
            print(f"    Status: {result['readiness_status']}")
            print(f"    Categories: {len(result['categories'])}")
            break  # Just test one season that has data

def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("  INVENTORY AGENT TOOLS - TEST SUITE")
    print("  Testing retail_store_inventory index")
    print("="*80)
    
    # Test connection first
    if not test_elasticsearch_connection():
        print("\n✗ Cannot proceed without Elasticsearch connection")
        return
    
    # Run all tests
    try:
        test_inventory_statistics()
        test_check_product_inventory()
        test_search_by_category()
        test_low_stock_alerts()
        test_regional_inventory()
        test_demand_forecast()
        test_seasonal_analysis()
        
        print("\n" + "="*80)
        print("  ✓ ALL TESTS COMPLETED")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n✗ Test suite failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
