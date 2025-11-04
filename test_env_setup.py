#!/usr/bin/env python3
"""Test environment setup and .env loading."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from current directory
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Check if variables are loaded
api_key = os.getenv('OPENAI_API_KEY')

print('Environment Setup Check:')
print('=' * 60)
print(f'✓ .env file: {"Found" if env_path.exists() else "Not found"}')
print(f'✓ .env.example: {"Found" if Path(".env.example").exists() else "Not found"}')
print(f'✓ .gitignore: {"Found" if Path(".gitignore").exists() else "Not found"}')
print('=' * 60)
print(f'OPENAI_API_KEY: {"Set" if api_key else "Not set"}')

if api_key:
    # Don't print the actual key, just validate format
    is_valid = api_key.startswith('sk-')
    masked = api_key[:8] + '*' * (len(api_key) - 12) + api_key[-4:] if len(api_key) > 12 else '***'
    print(f'  Format: {"Valid ✓" if is_valid else "Invalid ✗ (should start with sk-)"}')
    print(f'  Value: {masked}')
    print(f'  Length: {len(api_key)} characters')
    print()
    print('✓ Memory service will be fully operational!')
else:
    print()
    print('ℹ️  To enable full memory functionality:')
    print('   1. Get API key from: https://platform.openai.com/api-keys')
    print('   2. Edit .env file and add: OPENAI_API_KEY=sk-your-key-here')
    print('   3. Restart the application')
    print()
    print('⚠️  Without API key: Memory gracefully degrades (app still works)')

print('=' * 60)
