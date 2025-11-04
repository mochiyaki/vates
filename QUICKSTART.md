# Quick Start Guide - MemVerge Integration

Get up and running with MemVerge MemMachine integration in 5 minutes!

## Step 1: Add Your OpenAI API Key (Optional but Recommended)

```bash
# Edit the .env file
nano .env

# Add your key (replace the placeholder):
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

**Get your API key**: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

**Note**: The app works without this, but memory won't persist.

## Step 2: Verify Environment Setup

```bash
source .venv/bin/activate
python test_env_setup.py
```

You should see:
- ✓ `.env file: Found`
- ✓ `OPENAI_API_KEY: Set` (if you added the key)

## Step 3: Run Tests

```bash
pytest tests/ -v
```

**With API key**: All 9 tests pass ✓
**Without API key**: 5 pass, 4 skip (graceful degradation) ⚠️

## Step 4: Run Demo

```bash
python test_memverge_demo.py
```

This demonstrates:
- User preference storage
- Project completion tracking
- Creative prompt learning
- Memory retrieval

## Step 5: Start the Server

```bash
uvicorn narrative_architect.main:app --reload
```

Server starts at: [http://localhost:8000](http://localhost:8000)

## Step 6: Test API with Memory

### Create a Project with User ID

```bash
# Create a sample bundle first (if you don't have one)
cd /tmp
mkdir test_assets
echo "A journey begins" > test_assets/story.txt
zip -r bundle.zip test_assets/

# Upload with user_id
curl -X POST http://localhost:8000/projects \
  -F "bundle=@bundle.zip" \
  -F "user_id=alice"
```

Response:
```json
{
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued"
}
```

### Check Project Status

```bash
# Replace with your project_id from above
curl http://localhost:8000/projects/550e8400-e29b-41d4-a716-446655440000
```

The response includes `user_id: "alice"` - memory is now tracking this user!

## What's Next?

### Explore the Integration

- 📚 Read [MEMVERGE_INTEGRATION.md](MEMVERGE_INTEGRATION.md) - Full integration guide
- 🔧 Read [ENV_SETUP.md](ENV_SETUP.md) - Environment configuration details
- 💡 Check [test_memverge_demo.py](test_memverge_demo.py) - Example code

### Use Cases

**Personalized Narratives**:
```bash
# User "alice" creates multiple projects
# MemMachine remembers her style preferences
# Future narratives adapt to her preferences
```

**Cross-Session Learning**:
```bash
# Session 1: Create project with space theme
# Session 2: MemMachine suggests related themes
# Session 3: Builds on previous narratives
```

**Team Collaboration**:
```bash
# Each team member has a user_id
# Memory tracks individual preferences
# Shared project history available
```

## Troubleshooting

### Memory not working?

**Check**: Is `OPENAI_API_KEY` set?
```bash
python test_env_setup.py
```

**Solution**: Add key to `.env` file

### Tests skipping?

**This is expected** without API key! The app gracefully degrades.

**To fix**: Add `OPENAI_API_KEY` to `.env`

### API errors?

**Check**: Is the server running?
```bash
curl http://localhost:8000/healthz
# Should return: {"status": "ok"}
```

## Files Created

```
/home/yab/Vates/
├── .env                          # Your API key (never commit!)
├── .env.example                  # Template (safe to commit)
├── .gitignore                    # Protects .env from git
├── ENV_SETUP.md                  # Environment setup guide
├── MEMVERGE_INTEGRATION.md       # Full integration docs
├── QUICKSTART.md                 # This file
├── test_env_setup.py             # Check environment
├── test_memverge_demo.py         # Demo script
├── src/narrative_architect/
│   ├── services/
│   │   └── memory_service.py     # MemVerge integration
│   └── config.py                 # Loads .env on startup
└── tests/
    └── test_memory_integration.py # Memory tests
```

## Summary

✅ **Created**: Environment configuration (`.env`)
✅ **Configured**: Auto-loads on startup
✅ **Protected**: `.gitignore` prevents leaks
✅ **Tested**: All tests pass (with API key)
✅ **Documented**: Comprehensive guides available

You're ready to use MemVerge MemMachine with Narrative Architect! 🚀
