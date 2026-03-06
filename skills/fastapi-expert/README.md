# FastAPI Expert

Senior FastAPI specialist for building high-performance async Python APIs with Pydantic V2, async SQLAlchemy, and production-grade patterns.

## What This Skill Does

- **API Design**: Build REST endpoints with FastAPI's async router and dependency injection
- **Schema Validation**: Create Pydantic V2 models with field validators, model validators, and model_config
- **Async Database**: Set up async SQLAlchemy with CRUD operations and Alembic migrations
- **Authentication**: Implement JWT/OAuth2 authentication and authorization flows
- **WebSockets**: Create real-time WebSocket endpoints with proper lifecycle management
- **Testing**: Write async test suites with pytest-asyncio and httpx

## Installation

### Option 1: Download the `.skill` file (Easiest)

Download `fastapi-expert.skill` from this directory and place it in your skills folder:

```bash
cp fastapi-expert.skill ~/.claude/skills/
```

### Option 2: Copy the skill folder

```bash
cp -r skills/fastapi-expert ~/.claude/skills/
```

## What's Included

```
fastapi-expert/
├── SKILL.md                              # Core skill with workflow and constraints
├── references/
│   ├── pydantic-v2.md                    # Schemas, validation, model_config
│   ├── async-sqlalchemy.md               # Async database models and CRUD operations
│   ├── endpoints-routing.md              # APIRouter, dependencies, routing patterns
│   ├── authentication.md                 # JWT, OAuth2, get_current_user
│   ├── testing-async.md                  # pytest-asyncio, httpx, async fixtures
│   └── migration-from-django.md          # Migrating from Django/DRF to FastAPI
```

## Example Prompts

```
Build a FastAPI REST API for a task management app with user registration,
JWT login, and CRUD endpoints for tasks. Use async SQLAlchemy with PostgreSQL,
Pydantic V2 schemas for request/response validation, and proper error handling.
```

```
I'm migrating a Django REST Framework app to FastAPI. The app has user auth
with permissions, several model serializers, and ViewSets. Help me convert
the serializers to Pydantic V2 models and the views to async FastAPI endpoints.
```

## Platform Compatibility

| Platform | Status | Notes |
|----------|--------|-------|
| Claude Code | Full support | Copy to `~/.claude/skills/` |
| Claude.ai | Full support | Upload SKILL.md as project knowledge |
| Other LLM platforms | Full | Use SKILL.md content as system prompt |

## Related Skills

- **Fullstack Guardian** - Full-stack feature implementation across frontend and backend
- **Django Expert** - Alternative Python web framework for rapid development
- **Test Master** - Comprehensive testing strategies beyond API-specific tests
