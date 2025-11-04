# Environment Setup Guide

This guide explains how to set up your environment variables for the Narrative Architect with MemVerge integration.

## Quick Setup

### 1. Copy the Example Environment File

```bash
cp .env.example .env
```

### 2. Edit the `.env` File

Open `.env` in your editor and add your OpenAI API key:

```bash
# For vim
vim .env

# For nano
nano .env

# For VS Code
code .env
```

### 3. Add Your OpenAI API Key

Replace the placeholder with your actual API key:

```bash
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

**Where to get your API key:**
- Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- Log in or sign up for OpenAI
- Click "Create new secret key"
- Copy the key and paste it in `.env`

### 4. Verify Setup

Test that the environment is loaded correctly:

```bash
source .venv/bin/activate
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key loaded:', 'Yes' if os.getenv('OPENAI_API_KEY') else 'No')"
```

You should see: `API Key loaded: Yes`

## Environment Variables Reference

### Required for Full Memory Functionality

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for MemMachine embeddings | For memory persistence | `sk-proj-abc123...` |

### Optional

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `NARRATIVE_ARCHITECT_BASE` | Base directory for the application | `/home/yab/Vates` | `/custom/path` |

## Testing with Environment Variables

### Run All Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run tests
pytest tests/ -v
```

With `OPENAI_API_KEY` set, all 9 tests should pass:
- ✓ 9 passed (previously 5 passed, 4 skipped)

### Run Demo Script

```bash
python test_memverge_demo.py
```

With the API key set, you should see:
- ✓ Memory service initialized successfully
- ✓ Context retrieved from memory
- ✓ Similar projects found

## Running the Application

### Start the Server

```bash
# The .env file is automatically loaded by config.py
uvicorn narrative_architect.main:app --reload
```

### Test with API Request

```bash
# Create a project with user memory
curl -X POST http://localhost:8000/projects \
  -F "bundle=@path/to/your/bundle.zip" \
  -F "user_id=alice"
```

## Security Best Practices

### ✅ Do's

- ✅ Keep `.env` file in `.gitignore` (already configured)
- ✅ Use different API keys for development and production
- ✅ Rotate API keys regularly
- ✅ Use `.env.example` to document required variables
- ✅ Share `.env.example` with your team (no secrets)

### ❌ Don'ts

- ❌ Never commit `.env` to git
- ❌ Never share your `.env` file
- ❌ Never hardcode API keys in source code
- ❌ Never share API keys in chat/email/slack

## Troubleshooting

### Issue: "Memory service not available"

**Symptom**: Tests skip or demo shows warnings

**Cause**: `OPENAI_API_KEY` not set or invalid

**Solution**:
1. Check `.env` file exists: `ls -la .env`
2. Check key is set: `cat .env | grep OPENAI_API_KEY`
3. Verify format: Key should start with `sk-`
4. Test loading: `python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"`

### Issue: "Invalid API key"

**Symptom**: Memory operations fail with authentication error

**Cause**: Invalid or expired API key

**Solution**:
1. Generate new key at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Replace in `.env` file
3. Restart application

### Issue: Changes to `.env` not taking effect

**Symptom**: Old values still being used

**Solution**:
1. Restart the application (the .env is loaded on startup)
2. For tests, they load fresh each time
3. Check you're editing the right `.env` file (in project root)

## Advanced Configuration

### Using Environment Variables Directly

Instead of `.env` file, you can export variables:

```bash
export OPENAI_API_KEY="sk-your-key-here"
export NARRATIVE_ARCHITECT_BASE="/custom/path"

# Run application
uvicorn narrative_architect.main:app --reload
```

### Docker Environment

If running in Docker, pass environment variables:

```dockerfile
# Dockerfile
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
```

```bash
# docker-compose.yml
environment:
  - OPENAI_API_KEY=${OPENAI_API_KEY}
```

### Production Deployment

For production, use secure secret management:

- **AWS**: AWS Secrets Manager or Parameter Store
- **Google Cloud**: Secret Manager
- **Azure**: Key Vault
- **Kubernetes**: Sealed Secrets or External Secrets Operator
- **Heroku**: Config Vars
- **Vercel**: Environment Variables

## Cost Considerations

### OpenAI API Pricing

MemMachine uses OpenAI embeddings for semantic search:

- **Model**: text-embedding-ada-002 (default)
- **Cost**: ~$0.0001 per 1K tokens
- **Typical usage**:
  - Storing user preference: ~50 tokens (~$0.000005)
  - Storing project completion: ~200 tokens (~$0.00002)
  - Searching memories: ~100 tokens (~$0.00001)

### Free Tier & Limits

- OpenAI free trial: $5 credit (typically 3 months)
- Pay-as-you-go: Billed monthly
- Rate limits: Depends on account tier

### Cost Optimization

To reduce costs:
1. Use memory selectively (only for logged-in users)
2. Batch memory operations when possible
3. Set memory retention limits
4. Monitor usage via OpenAI dashboard

## Alternative: Running Without API Key

The application works without `OPENAI_API_KEY`:

### Graceful Degradation

- ✅ All core features work
- ✅ Narrative generation works
- ✅ API endpoints work
- ⚠️ Memory persistence disabled
- ⚠️ No cross-session learning

### When to Skip Memory

Good for:
- Development testing
- CI/CD pipelines
- Cost-sensitive deployments
- Single-session usage

## Files Overview

```
/home/yab/Vates/
├── .env                 # Your secrets (never commit!)
├── .env.example         # Template (safe to commit)
├── .gitignore           # Prevents .env from being committed
├── src/
│   └── narrative_architect/
│       └── config.py    # Loads .env on startup
└── tests/
    └── test_memory_integration.py  # Tests gracefully skip without API key
```

## Summary

1. ✅ Copy `.env.example` to `.env`
2. ✅ Add your `OPENAI_API_KEY`
3. ✅ Never commit `.env` to git
4. ✅ Start the application - environment loads automatically!

For questions or issues, check:
- [MemMachine Docs](https://docs.memmachine.ai)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [MEMVERGE_INTEGRATION.md](MEMVERGE_INTEGRATION.md) for integration details
