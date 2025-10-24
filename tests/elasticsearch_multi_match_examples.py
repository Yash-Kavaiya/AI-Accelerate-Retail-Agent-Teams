"""
Elasticsearch Multi-Match Query Example
Demonstrates the multi_match query pattern from Elasticsearch docs for retail_store_inventory
"""

from elasticsearch import Elasticsearch

# Initialize Elasticsearch client
client = Elasticsearch(
    "https://my-elasticsearch-project-e0ae1f.es.us-central1.gcp.elastic.cloud:443",
    api_key="LTB4NkZKb0JDNDR2WWhEalo3Qlg6d3o1LUVZazBYMm5WSFhKYjlFZldPUQ=="
)

# Example 1: Using retriever with multi_match (Recommended for Elasticsearch 8+)
print("="*80)
print("Example 1: Multi-Match Query with Retriever Pattern")
print("="*80)

retriever_object = {
    "standard": {
        "query": {
            "multi_match": {
                "query": "Electronics",  # Search term
                "fields": ["Category"]    # Fields to search in
            }
        }
    }
}

search_response = client.search(
    index="retail_store_inventory",
    retriever=retriever_object,
    size=5
)

print(f"\nFound {search_response['hits']['total']['value']} products")
print("\nTop 5 Results:")
for hit in search_response['hits']['hits']:
    source = hit['_source']
    print(f"  Product {source['Product ID']}: {source['Category']} - "
          f"{source['Inventory Level']} units in stock")

# Example 2: Multi-Match with Boolean Filters
print("\n" + "="*80)
print("Example 2: Multi-Match + Filters (Region + Inventory Range)")
print("="*80)

retriever_with_filters = {
    "standard": {
        "query": {
            "bool": {
                "must": [{
                    "multi_match": {
                        "query": "Furniture",
                        "fields": ["Category"]
                    }
                }],
                "filter": [
                    {"term": {"Region": "North"}},
                    {"range": {"Inventory Level": {"gte": 100}}}
                ]
            }
        }
    }
}

search_response = client.search(
    index="retail_store_inventory",
    retriever=retriever_with_filters,
    size=5
)

print(f"\nFound {search_response['hits']['total']['value']} Furniture products in North region with 100+ units")
print("\nTop 5 Results:")
for hit in search_response['hits']['hits']:
    source = hit['_source']
    print(f"  Product {source['Product ID']}: Store {source['Store ID']} - "
          f"{source['Inventory Level']} units (Region: {source['Region']})")

# Example 3: Traditional Search Body (Alternative pattern)
print("\n" + "="*80)
print("Example 3: Traditional Search Body Pattern")
print("="*80)

search_body = {
    "query": {
        "bool": {
            "must": [{
                "multi_match": {
                    "query": "Toys",
                    "fields": ["Category"]
                }
            }],
            "filter": [
                {"term": {"Region": "South"}}
            ]
        }
    },
    "size": 5,
    "sort": [{"Inventory Level": {"order": "desc"}}]
}

search_response = client.search(
    index="retail_store_inventory",
    body=search_body
)

print(f"\nFound {search_response['hits']['total']['value']} Toys in South region")
print("\nTop 5 by Inventory Level:")
for hit in search_response['hits']['hits']:
    source = hit['_source']
    print(f"  Product {source['Product ID']}: {source['Inventory Level']} units - "
          f"Store {source['Store ID']} (${source['Price']:.2f})")

# Example 4: Aggregations for Statistics
print("\n" + "="*80)
print("Example 4: Multi-Match with Aggregations")
print("="*80)

search_body_with_aggs = {
    "query": {
        "multi_match": {
            "query": "Electronics",
            "fields": ["Category"]
        }
    },
    "size": 0,  # Don't return documents, just aggregations
    "aggs": {
        "total_inventory": {
            "sum": {"field": "Inventory Level"}
        },
        "total_sold": {
            "sum": {"field": "Units Sold"}
        },
        "avg_price": {
            "avg": {"field": "Price"}
        },
        "regions": {
            "terms": {"field": "Region", "size": 10}
        }
    }
}

search_response = client.search(
    index="retail_store_inventory",
    body=search_body_with_aggs
)

aggs = search_response['aggregations']
print(f"\nElectronics Category Statistics:")
print(f"  Total Products: {search_response['hits']['total']['value']}")
print(f"  Total Inventory: {int(aggs['total_inventory']['value'])} units")
print(f"  Total Units Sold: {int(aggs['total_sold']['value'])}")
print(f"  Average Price: ${aggs['avg_price']['value']:.2f}")

print(f"\n  Distribution by Region:")
for bucket in aggs['regions']['buckets']:
    print(f"    {bucket['key']}: {bucket['doc_count']} products")

print("\n" + "="*80)
print("Examples Complete!")
print("="*80)

# Key Takeaways
print("""
KEY PATTERNS USED:

1. RETRIEVER PATTERN (Elasticsearch 8+):
   retriever_object = {
       "standard": {
           "query": {
               "multi_match": {
                   "query": "search_term",
                   "fields": ["field_name"]
               }
           }
       }
   }
   
2. BOOLEAN QUERIES (Combining multi_match + filters):
   "bool": {
       "must": [multi_match_query],
       "filter": [term_filters, range_filters]
   }

3. TRADITIONAL SEARCH BODY (For sorting):
   body = {
       "query": {...},
       "size": 10,
       "sort": [{"field": {"order": "asc"}}]
   }

4. AGGREGATIONS (For statistics):
   "aggs": {
       "stat_name": {"sum/avg/terms": {"field": "field_name"}}
   }

Note: Cannot combine retriever + sort in same query!
Use traditional search body when sorting is needed.
""")
