# iAngel Alpha Backend - Context for Gemini

## ⚠️ PROTOCOLE & RÈGLES D'OR (MANDATAIRE) ⚠️

> **VISION OUTSIDE-IN :** "Est-ce que Ginette va se sentir plus protégée avec la journée qu'on a passée aujourd'hui ?"

1.  **HONNÊTETÉ RADICALE (NO BULLSHIT) :**
    *   Interdiction formelle de "maquiller" ou "nuancer" la vérité pour plaire.
    *   Une erreur assumée est un outil de travail. Une erreur cachée est un sabotage.
    *   Si une tâche échoue ou dévie, dites-le immédiatement, sans enrobage.

2.  **ROBUSTESSE > VITESSE :**
    *   Le temps n'est pas un facteur de décision limitant.
    *   Prenez le double du temps s'il le faut, mais livrez un résultat "béton", pas un "maquillage de surface".
    *   Ne jamais sacrifier la profondeur technique pour une victoire rapide.

3.  **INITIATIVE INTELLIGENTE :**
    *   L'initiative est encouragée SI elle est analysée, justifiée et **transparentement rapportée**.
    *   Ne jamais "faire croire" que tout était prévu si c'était une improvisation (même réussie).

4.  **MISSION SOCIALE (GINETTE) :**
    *   Nous ne codons pas pour un client, mais pour protéger une personne vulnérable.
    *   Chaque ligne de code, chaque log, chaque erreur doit être pensé pour réduire l'anxiété de l'utilisateur final.

---

## Project Overview
**iAngel** is a digital guardian angel designed for technologically vulnerable seniors in Quebec. It prioritizes empathy, patience, and "one step at a time" guidance over speed or efficiency.
This repository contains the **Backend API** (Python/FastAPI) that powers the iOS client (separate repo).

**Core Philosophy:**
*   **Empathy First:** Error messages and interactions must be warm, reassuring, and non-technical.
*   **One Step at a Time:** The reasoning engine validates each step before moving to the next.
*   **Privacy:** Strict data retention policies (7-day purge).

## Technology Stack
*   **Language:** Python 3.11+
*   **Framework:** FastAPI
*   **Package Manager:** `uv` (Astral)
*   **LLM:** Anthropic Claude 3.5 Sonnet (`claude-3-5-sonnet-20241022`)
*   **Deployment:** Railway (PaaS)
*   **State Management:** InMemory (S0) -> PostgreSQL (S2)

## Project Structure (Architecture S0-Stable)
```
iangel-alpha/
├── app/
│   ├── main.py           # Application entry point & factory
│   ├── config.py         # Pydantic settings & env vars
│   ├── api/
│   │   ├── router.py     # Main API router
│   │   └── v1/endpoints/ # Route definitions (health, capture)
│   ├── core/
│   │   ├── errors.py     # Custom empathic exceptions
│   │   ├── middleware.py # Safety net & X-Request-ID
│   │   ├── state.py      # State Management (InMemoryStore)
│   │   ├── probes.py     # Health Check Probes Interface
│   │   ├── reasoning.py  # Core logic for step-by-step guidance
│   │   └── llm/          # LLM provider abstractions
│   ├── models/           # Pydantic schemas (requests/responses)
│   ├── sandbox/          # Mock data loader for testing/dev (Phase P4)
│   └── services/         # Business logic (Orchestrators)
│       ├── capture_service.py # Orchestrates LLM + State + Mock
│       └── health_service.py  # Orchestrates Probes
├── tests/                # Pytest suite (Integration + Unit)
├── mocks/                # JSON mock files for sandbox mode
├── Officials_docs/       # Detailed project documentation
├── pyproject.toml        # Dependencies & tool configuration
└── railway.toml          # Deployment configuration
```

## Key Features & Phases
*   **S0-01 (Done):** Structure, Robustness Tests, Middleware Safety Net.
*   **S0-02 (Done):** Smart Health Check with Probes & Empathic Messages.
*   **S0-03 (Done):** Capture Endpoint with State Persistence, Sandbox Gatekeeper & **Voice-Ready Fields** (`input_modality`, `spoken_message`).
*   **S0-04 (Done):** Mock Loader & Scenarios enriched for voice interaction.

## Development Conventions
*   **Dependency Management:** Use `uv` strictly.
*   **Code Quality:**
    *   **Linting:** `uv run ruff check app/`
    *   **Type Checking:** `uv run mypy app/` (Strict mode)
    *   **Testing:** `uv run pytest tests/` (Must pass all 85+ tests)
*   **Running Locally:**
    ```bash
    uv run uvicorn app.main:app --reload --port 8000
    ```
*   **Configuration:**
    *   `SANDBOX_MODE=True` uses local mocks (no cost).
    *   `SANDBOX_MODE=False` calls Anthropic (requires API Key).

## Documentation
Refer to `Officials_docs/PHASE_S0_COMPLETION_REPORT.md` for the technical audit of the current state.
Old briefs in `Officials_docs/scripts/` are for reference only.