# GitHub Copilot Instructions - iAngel Alpha Backend

## Repository Overview

**iAngel** is a digital guardian angel designed for technologically vulnerable seniors in Quebec. This backend API (Python/FastAPI) powers an iOS client and prioritizes empathy, patience, and "one step at a time" guidance over speed.

**Mission-Critical Philosophy (From GEMINI.md):**
- **HONNÊTETÉ RADICALE**: Never hide errors or nuance the truth. An assumed error is a work tool; a hidden error is sabotage.
- **ROBUSTESSE > VITESSE**: Take double the time if needed, but deliver solid results. Never sacrifice technical depth for quick wins.
- **MISSION SOCIALE**: We code to protect vulnerable people (Ginette), not just for clients. Every line of code must reduce end-user anxiety.

## Technology Stack & Requirements

- **Language**: Python 3.11+ (tested with 3.12.3)
- **Framework**: FastAPI
- **Package Manager**: `uv` (Astral) - **MANDATORY**, do not use pip/poetry
- **LLM**: Anthropic Claude 3.5 Sonnet
- **Database**: PostgreSQL (Phase S2), currently InMemory (Phase S0)
- **Deployment**: Railway PaaS
- **Testing**: pytest with 100 tests (must all pass)
- **Linting**: ruff (23 known warnings are acceptable)
- **Type Checking**: mypy strict mode (5 known errors are acceptable)

## Critical Build & Validation Workflow

### 1. Initial Setup (Required Once)
```bash
# Install uv if not available (official method)
curl -LsSf https://astral.sh/uv/install.sh | sh

# OR use pip as fallback
pip install uv

# Install all dependencies (takes ~60 seconds)
uv sync
```

**Important**: `uv sync` creates a `.venv` directory. Always use `uv run` to execute commands.

### 2. Before Making Changes
```bash
# ALWAYS run tests first to establish baseline (takes ~1 second)
uv run pytest tests/ -v

# Check linting baseline (takes ~3 seconds)
uv run ruff check app/

# Check type hints baseline (takes ~10 seconds)
uv run mypy app/
```

**Known Acceptable Issues:**
- **ruff**: 23 warnings (B008 for FastAPI Depends, B904 for exception chaining, etc.)
- **mypy**: 5 errors (unused type ignores, missing return annotations)
- **pytest**: All 100 tests MUST pass

### 3. Running the Application Locally
```bash
# Development mode with auto-reload (default sandbox mode)
uv run uvicorn app.main:app --reload --port 8000

# Or use the convenience script
./start_server.sh

# Access API docs at: http://localhost:8000/docs
# Health check: http://localhost:8000/api/v1/health
```

### 4. After Making Changes
```bash
# ALWAYS run tests after code changes
uv run pytest tests/ -v

# Check for new linting issues
uv run ruff check app/

# Check for new type issues
uv run mypy app/

# If tests fail, fix issues before committing
```

### 5. Environment Configuration
```bash
# Copy example environment file
cp .env.example .env

# Key variables:
# - SANDBOX_MODE=true (uses mocks, no API costs)
# - SANDBOX_MODE=false (requires ANTHROPIC_API_KEY)
# - DEBUG=true (verbose logging)
```

## Project Architecture

### Directory Structure
```
iangel-alpha/
├── app/
│   ├── main.py              # FastAPI app factory, CORS, lifespan
│   ├── config.py            # Pydantic settings (env vars)
│   ├── api/
│   │   ├── router.py        # Main API router
│   │   └── v1/endpoints/    # Health & Capture endpoints
│   ├── core/
│   │   ├── errors.py        # Custom empathic exceptions
│   │   ├── middleware.py    # Safety net, X-Request-ID
│   │   ├── state.py         # InMemoryStateStore, ReasoningEngine
│   │   ├── reasoning.py     # Step-by-step guidance logic
│   │   ├── probes.py        # Health check probe interface
│   │   ├── database.py      # SQLAlchemy async session
│   │   └── llm/             # LLM provider abstractions
│   │       ├── base.py      # Abstract LLMProvider
│   │       ├── claude.py    # Anthropic client with retry
│   │       ├── schemas.py   # LLM request/response models
│   │       └── utils.py     # Prompt formatting
│   ├── models/
│   │   ├── schemas.py       # Pydantic request/response models
│   │   └── database.py      # SQLAlchemy ORM models (Phase S2)
│   ├── services/
│   │   ├── capture_service.py   # Main business logic orchestrator
│   │   └── health_service.py    # Health check aggregator
│   ├── sandbox/
│   │   └── mock_loader.py   # Loads JSON mocks for testing
│   └── infrastructure/
│       └── probes.py        # Concrete health check probes
├── tests/                   # 100 pytest tests (unit + integration)
├── mocks/                   # JSON mock scenarios (M01-M04)
├── Officials_docs/          # Technical documentation
├── pyproject.toml           # Dependencies, ruff, mypy, pytest config
├── railway.toml             # Railway deployment config
├── Dockerfile               # Multi-stage build with uv
├── .env.example             # Environment template
└── start_server.sh          # Convenience script for dev server
```

### Key Configuration Files
- **pyproject.toml**: All tool configuration (ruff, mypy, pytest, dependencies)
- **.env**: Environment variables (NEVER commit, use .env.example)
- **railway.toml**: Deployment configuration for Railway PaaS
- **Dockerfile**: Multi-stage build optimized for uv

## Development Conventions (From GEMINI.md & codebase)

### Code Style
- **Strict typing**: Use type hints everywhere (mypy strict mode)
- **Error messages**: Must be empathic, warm, non-technical (see `app/core/errors.py`)
- **Dependency injection**: Use FastAPI `Depends()` for services
- **Async everywhere**: All I/O operations use `async/await`
- **French comments in code**: Business logic comments in French, docstrings in French
- **English for technical terms**: Variable names, function names, etc.

### Testing Standards
- **100% test pass rate**: No exceptions
- **Isolation**: Each test is independent
- **Mocking**: Use `SANDBOX_MODE=true` for free testing
- **Coverage**: Aim for 80%+ (configured in pyproject.toml)

### Error Handling
- **Never crash**: Middleware catches all exceptions
- **Empathic messages**: Use custom exceptions from `app/core/errors.py`
- **Request ID**: Always include `X-Request-ID` in responses
- **Hide tech details**: Production mode hides stack traces

## Common Issues & Workarounds

### Issue: uv not found
**Solution**: Install via official installer: `curl -LsSf https://astral.sh/uv/install.sh | sh` or fallback to pip: `pip install uv`

### Issue: Tests fail after fresh clone
**Solution**: Run `uv sync` first to install dependencies

### Issue: "Module not found" errors
**Solution**: Always use `uv run` prefix for commands

### Issue: mypy reports 5+ errors
**Solution**: Check if they're the known 5 errors (see baseline above). New errors need fixing.

### Issue: ruff reports 100+ warnings
**Solution**: The baseline is 23 warnings. New warnings need addressing.

### Issue: Server won't start - Port 8000 in use
**Solution**: Kill existing process: `lsof -ti:8000 | xargs kill -9`

### Issue: Claude API errors in tests
**Solution**: Ensure `SANDBOX_MODE=true` in `.env` or environment

### Warning: `tool.uv.dev-dependencies` deprecated
**Note**: This is a known deprecation warning. Can be ignored or migrate to `dependency-groups.dev` later.

## Phase Information (Current: S0-Stable)

The project follows a phased approach:
- **S0**: Walking skeleton with in-memory state (CURRENT)
- **S1**: Advanced reasoning engine with LLM
- **S2**: PostgreSQL persistence
- **S3**: Pedagogical safety features

See `Officials_docs/PHASE_S0_COMPLETION_REPORT.md` for detailed phase documentation.

## Critical Files to Review Before Changes

1. **GEMINI.md**: Core philosophy and development protocols
2. **README.md**: High-level project overview
3. **pyproject.toml**: All configuration and dependencies
4. **app/core/state.py**: State management and reasoning engine
5. **app/services/capture_service.py**: Main orchestration logic
6. **tests/conftest.py**: Test fixtures and configuration

## Trust These Instructions

These instructions have been validated by running all commands successfully. Only search for additional information if:
- You encounter an error not documented here
- You need to understand business logic (check `Officials_docs/`)
- You're working on a new feature not covered in Phase S0

**When in doubt, favor ROBUSTESSE over VITESSE. Better to take more time than to ship broken code.**
