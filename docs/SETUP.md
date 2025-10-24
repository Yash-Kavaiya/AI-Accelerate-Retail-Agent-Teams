# Quick Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Elasticsearch Cloud account (or self-hosted Elasticsearch 8.0+)
- Google API key for Gemini

## Step 1: Install Dependencies

```bash
# Install all required packages
pip install -r requirement.txt

# Or install individually
pip install google-adk
pip install elasticsearch>=8.0.0
pip install python-dotenv>=1.0.0
```

## Step 2: Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your credentials:
```bash
# Windows
notepad .env

# Or use any text editor
```

3. Add your credentials:
```env
ELASTICSEARCH_CLOUD_URL=https://your-cluster.es.region.provider.elastic.cloud:443
ELASTICSEARCH_API_KEY=your_base64_encoded_key
GOOGLE_API_KEY=your_google_api_key
```

### Getting Elasticsearch Credentials

1. Log in to [Elasticsearch Cloud](https://cloud.elastic.co/)
2. Navigate to your deployment
3. Go to **Management** → **Security** → **API Keys**
4. Click **Create API Key**
5. Give it a name (e.g., "Review Analysis Agent")
6. Set permissions to **read** for your index
7. Copy the **Base64 encoded** key

### Getting Google API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click **Create API Key**
3. Copy the generated key

## Step 3: Verify Installation

Run the test suite to verify everything is working:

```bash
python test_review_agent_tools.py
```

Expected output:
```
==================================================
REVIEW TEXT ANALYSIS AGENT - ELASTICSEARCH TOOLS TEST
==================================================

✅ Elasticsearch URL configured
✅ API Key configured

[Tests running...]

==================================================
TEST SUMMARY
==================================================
✅ PASSED: Semantic Search
✅ PASSED: Rating Filter
✅ PASSED: Aggregate Statistics
✅ PASSED: Department Filter
✅ PASSED: Class Filter

Total: 5/5 tests passed
🎉 All tests passed! The agent is ready to use.
```

## Step 4: Run the Agent

### Option 1: Interactive CLI

```bash
adk run retail-agents-team/review_text_analysis_agent
```

Then type your queries:
```
> Find reviews about comfortable fabric
> What's the average rating for dresses?
> Show me negative reviews about sizing
```

### Option 2: Web Interface

```bash
adk web
```

Then:
1. Open your browser to the displayed URL (usually http://localhost:8000)
2. Select "review_text_analysis_agent" from the list
3. Start chatting with the agent

## Step 5: Try Example Queries

### Semantic Search
```
Find reviews mentioning fabric quality and comfort
```

### Rating Analysis
```
What do customers say in 5-star reviews?
```

### Statistical Overview
```
Give me a statistical overview of all reviews
```

### Department Analysis
```
Analyze reviews for the Tops department
```

### Combined Analysis
```
Find negative reviews about sizing issues in the Dresses category
```

## Troubleshooting

### Import Error: elasticsearch

**Problem**: `ModuleNotFoundError: No module named 'elasticsearch'`

**Solution**:
```bash
pip install elasticsearch>=8.0.0
```

### Import Error: google.adk

**Problem**: `ModuleNotFoundError: No module named 'google.adk'`

**Solution**:
```bash
pip install google-adk
```

### Connection Error

**Problem**: Cannot connect to Elasticsearch

**Solutions**:
1. Verify your `ELASTICSEARCH_CLOUD_URL` is correct
2. Check your API key is valid
3. Ensure your IP is whitelisted in Elasticsearch Cloud
4. Test connection with curl:
   ```bash
   curl -H "Authorization: ApiKey YOUR_KEY" YOUR_URL/_cluster/health
   ```

### Authentication Error

**Problem**: `401 Unauthorized`

**Solutions**:
1. Regenerate API key in Elasticsearch Console
2. Make sure you copied the **Base64 encoded** version
3. Check API key has read permissions for the index

### No Results

**Problem**: Queries return 0 results

**Solutions**:
1. Verify index name is `womendressesreviewsdataset`
2. Check data exists in your index:
   ```bash
   curl -H "Authorization: ApiKey YOUR_KEY" YOUR_URL/womendressesreviewsdataset/_count
   ```
3. Ensure semantic fields are populated

### ADK Not Found

**Problem**: `adk: command not found`

**Solutions**:
1. Install ADK globally:
   ```bash
   pip install google-adk
   ```
2. Or use Python module syntax:
   ```bash
   python -m google.adk.cli run retail-agents-team/review_text_analysis_agent
   ```

## Verify Everything Works

Run this quick checklist:

- [ ] Python 3.8+ installed: `python --version`
- [ ] Dependencies installed: `pip list | grep elasticsearch`
- [ ] `.env` file created with credentials
- [ ] Test suite passes: `python test_review_agent_tools.py`
- [ ] ADK works: `adk --version`
- [ ] Agent runs: `adk run retail-agents-team/review_text_analysis_agent`

## Next Steps

Once everything is working:

1. Read the [README.md](retail-agents-team/review_text_analysis_agent/README.md) for usage guide
2. Check [ELASTICSEARCH_INTEGRATION.md](ELASTICSEARCH_INTEGRATION.md) for technical details
3. Review [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for architecture overview
4. Explore the agent's capabilities with different queries

## Getting Help

- **Elasticsearch Issues**: Check [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- **Google ADK Issues**: Check [ADK GitHub](https://github.com/google/adk-python)
- **Agent Specific**: Review documentation files in this repository

---

**Quick Reference Commands**:
```bash
# Install
pip install -r requirement.txt

# Test
python test_review_agent_tools.py

# Run
adk run retail-agents-team/review_text_analysis_agent

# Web UI
adk web
```
