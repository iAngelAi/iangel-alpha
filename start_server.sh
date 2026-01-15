#!/bin/bash
export SANDBOX_MODE=false
export ANTHROPIC_API_KEY=$(grep ANTHROPIC_API_KEY .env | cut -d '=' -f2)
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
