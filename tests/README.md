# Tests

This directory contains all test files for the AI Accelerate Retail Agent Teams project.

## Test Files

### Agent Tests
- `test_customer_support_agent_tools.py` - Tests for customer support agent functionality
- `test_inventory_agent_tools.py` - Tests for inventory agent functionality
- `test_review_agent_tools.py` - Tests for review text analysis agent functionality
- `test_shopping_agent_tools.py` - Tests for shopping agent functionality

### Infrastructure Tests
- `test_elasticsearch_connection.py` - Tests for Elasticsearch connectivity
- `test_faq_direct.py` - Direct FAQ functionality tests
- `elasticsearch_multi_match_examples.py` - Elasticsearch multi-match query examples

## Running Tests

To run all tests:
```bash
pytest
```

To run a specific test file:
```bash
pytest tests/test_customer_support_agent_tools.py
```

To run tests with verbose output:
```bash
pytest -v
```

To run tests with coverage:
```bash
pytest --cov=retail-agents-team
```

## Test Requirements

Make sure you have all required dependencies installed:
```bash
pip install -r ../requirement.txt
pip install pytest pytest-cov
```

## Configuration

Ensure your environment variables are properly set before running tests:
- Elasticsearch connection details
- API keys
- Other required credentials

See the main project documentation in `../docs/` for configuration details.
