# ═══════════════════════════════════════════════════════════════════════════
# Dockerfile — iAngel Alpha Backend
# Multi-stage build avec uv pour performance optimale
# ═══════════════════════════════════════════════════════════════════════════

# Stage 1: Dependencies (cached si lockfile inchangé)
FROM python:3.11-slim AS deps

# Installer uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copier uniquement les fichiers de dépendances pour cache optimal
COPY pyproject.toml uv.lock* ./

# Installer les dépendances (sans dev)
RUN uv sync --frozen --no-dev || uv sync --no-dev

# Stage 2: Application
FROM python:3.11-slim

WORKDIR /app

# Copier le venv depuis le stage deps
COPY --from=deps /app/.venv /app/.venv

# Ajouter le venv au PATH
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copier le code source
COPY app/ ./app/
COPY mocks/ ./mocks/

# Port exposé (Railway utilise $PORT)
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/api/v1/health').raise_for_status()" || exit 1

# Commande de démarrage (Railway override via railway.toml)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
