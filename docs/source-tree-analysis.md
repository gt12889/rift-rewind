# Source Tree Analysis

**Last Updated:** 2025-01-27

## Directory Structure

```
rift-rewind/
├── .bmad/                    # BMAD Method configuration and workflows
│   ├── bmb/                  # BMAD Builder module
│   ├── bmm/                  # BMAD Method Module
│   └── core/                 # BMAD Core
├── .cursor/                  # Cursor IDE configuration
├── .github/                   # GitHub workflows and templates
├── config/                    # Application configuration
│   ├── __init__.py
│   ├── settings.py          # ⭐ Pydantic settings and environment config
│   └── bedrock_agents/       # AWS Bedrock agent configurations
│       ├── comparison_agent.json
│       ├── insights_agent.json
│       ├── match_analysis_agent.json
│       ├── social_content_agent.json
│       ├── visualization_agent.json
│       ├── year_summary_agent.json
│       └── instructions/     # Agent instruction prompts
├── deploy/                    # Deployment infrastructure
│   ├── cloudformation.yaml  # ⭐ AWS CloudFormation template
│   └── deploy.sh            # Deployment script
├── docs/                     # Generated documentation (this folder)
│   ├── technical/           # Technical documentation
│   └── bmm-workflow-status.yaml
├── epics/                    # Epic definitions (BMAD workflow)
├── src/                      # ⭐ Main source code
│   ├── __init__.py
│   ├── agents/              # ⭐ Multi-agent system
│   │   ├── __init__.py
│   │   ├── base_agent.py   # Base agent class
│   │   ├── comparison_agent.py
│   │   ├── context_manager.py  # ⭐ Shared context management
│   │   ├── events.py        # Event bus implementation
│   │   ├── insights_agent.py
│   │   ├── match_analysis_agent.py
│   │   ├── messages.py      # Agent message types
│   │   ├── orchestrator.py  # ⭐ Central workflow orchestrator
│   │   ├── registry.py      # Agent registry
│   │   ├── social_content_agent.py
│   │   ├── visualization_agent.py
│   │   └── year_summary_agent.py
│   ├── analyzers/           # ⭐ Data analysis modules
│   │   ├── __init__.py
│   │   ├── match_analyzer.py  # Statistical match analysis
│   │   └── year_summary.py    # Year-end summary generation
│   ├── api/                  # ⭐ FastAPI application
│   │   ├── __init__.py
│   │   └── main.py          # ⭐ Main API endpoints and app setup
│   ├── generators/           # Content generation
│   │   ├── __init__.py
│   │   ├── social_content.py  # Social media content generation
│   │   └── visualizations.py  # Chart and visualization generation
│   └── services/             # ⭐ External service integrations
│       ├── __init__.py
│       ├── aws_bedrock.py   # ⭐ AWS Bedrock (Claude) integration
│       ├── aws_comprehend.py # ⭐ AWS Comprehend integration
│       └── riot_api.py       # ⭐ Riot Games API client
├── static/                    # Static frontend files
│   └── index.html           # Simple HTML frontend
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_agents.py
│   └── test_api.py
├── .gitignore
├── AGENT_BUILDER_INSTRUCTIONS.txt
├── AGENT_INSTRUCTIONS.md
├── AGENT_PROMPT_TEMPLATE.md
├── ARCHITECTURE.md           # Existing architecture documentation
├── CONTRIBUTING.md           # Contribution guidelines
├── Dockerfile                # Docker container definition
├── docker-compose.yml        # Docker Compose configuration
├── FEATURES.md               # Feature list
├── LICENSE                   # Apache 2.0 license
├── PROJECT_SUMMARY.md        # Project summary
├── QUICKSTART.md            # Quick start guide
├── README.md                # ⭐ Main project README
├── RUN_APP.md               # Run instructions
├── SETUP.md                 # Setup guide
├── main.py                  # ⭐ Application entry point
└── requirements.txt         # ⭐ Python dependencies
```

## Critical Folders

### `src/api/` - API Layer
**Purpose:** FastAPI application with REST endpoints

**Key Files:**
- `main.py`: Main FastAPI app, endpoint definitions, request/response models, CORS configuration

**Entry Point:** `main.py` defines the FastAPI `app` instance

**Integration Points:**
- Imports services from `src/services/`
- Uses analyzers from `src/analyzers/`
- Uses generators from `src/generators/`
- Delegates to orchestrator for multi-agent workflows

---

### `src/services/` - External Service Integrations
**Purpose:** Clients for external APIs and AWS services

**Key Files:**
- `riot_api.py`: Riot Games API client with rate limiting
- `aws_bedrock.py`: AWS Bedrock (Claude) integration for AI generation
- `aws_comprehend.py`: AWS Comprehend for sentiment analysis

**Integration Points:**
- Used by API endpoints and agents
- Configured via `config/settings.py`

---

### `src/agents/` - Multi-Agent System
**Purpose:** Specialized agents for different analysis tasks

**Key Files:**
- `orchestrator.py`: Central coordinator that manages workflows
- `context_manager.py`: Shared context system for agent communication
- `registry.py`: Agent registration and lookup
- `events.py`: Event bus for agent coordination
- `base_agent.py`: Base class for all agents
- Individual agent files: `match_analysis_agent.py`, `insights_agent.py`, etc.

**Architecture Pattern:** Multi-Agent System with Orchestrator pattern

**Integration Points:**
- Orchestrator delegates tasks to agents
- Agents use context manager for shared state
- Agents publish events via event bus

---

### `src/analyzers/` - Data Analysis
**Purpose:** Statistical analysis of match data

**Key Files:**
- `match_analyzer.py`: KDA, win rate, champion/role analysis, trend detection
- `year_summary.py`: Year-end aggregation and summary generation

**Integration Points:**
- Used by agents and API endpoints
- Processes data from Riot API

---

### `src/generators/` - Content Generation
**Purpose:** Generate visualizations and social media content

**Key Files:**
- `visualizations.py`: Plotly/Matplotlib chart generation
- `social_content.py`: Social media content formatting

**Integration Points:**
- Used by visualization and social content agents
- Returns base64-encoded images for API responses

---

### `config/` - Configuration
**Purpose:** Application settings and configuration

**Key Files:**
- `settings.py`: Pydantic settings loaded from environment variables
- `bedrock_agents/`: Agent instruction prompts and configurations

**Integration Points:**
- Imported by all services and API endpoints
- Environment variables loaded via `.env` file

---

### `deploy/` - Deployment
**Purpose:** Infrastructure as code and deployment scripts

**Key Files:**
- `cloudformation.yaml`: AWS CloudFormation template for Lambda, API Gateway, IAM roles
- `deploy.sh`: Deployment automation script

**Integration Points:**
- Defines AWS infrastructure for production deployment

---

## Entry Points

### Application Entry Point
**File:** `main.py`
**Purpose:** Starts the FastAPI application with Uvicorn

**Code:**
```python
if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
```

### API Entry Point
**File:** `src/api/main.py`
**Purpose:** FastAPI application instance and endpoint definitions

**Key Components:**
- FastAPI app initialization
- CORS middleware configuration
- Service initialization
- Agent system initialization
- Endpoint route definitions

---

## File Organization Patterns

### Service Layer Pattern
Services in `src/services/` follow a client pattern:
- Class-based clients (e.g., `RiotAPIClient`, `BedrockService`)
- Rate limiting and error handling
- Configuration via settings

### Agent Pattern
Agents in `src/agents/` follow a consistent structure:
- Inherit from `BaseAgent`
- Implement `handle_request()` method
- Use context manager for shared state
- Publish events via event bus

### Analyzer Pattern
Analyzers in `src/analyzers/` are stateless:
- Class-based with instance methods
- Pure functions for calculations
- Return structured dictionaries

---

## Integration Points

### API → Services
API endpoints directly call service clients for simple operations.

### API → Orchestrator → Agents
Complex workflows go through the orchestrator, which delegates to specialized agents.

### Agents → Context Manager
Agents read and write shared context for workflow coordination.

### Agents → Services
Agents use services (Bedrock, Comprehend) for AI operations.

### Agents → Analyzers
Agents use analyzers for statistical computations.

### Agents → Generators
Agents use generators for visualization and content creation.

---

## Critical Paths

### Request Flow (Player Insights)
1. `src/api/main.py` → `get_player_insights()` endpoint
2. `src/services/riot_api.py` → Fetch match data
3. `src/agents/orchestrator.py` → Coordinate workflow
4. `src/agents/match_analysis_agent.py` → Analyze matches
5. `src/agents/insights_agent.py` → Generate insights
6. `src/agents/visualization_agent.py` → Create charts
7. Return combined response

### Request Flow (Year Summary)
1. `src/api/main.py` → `get_year_summary()` endpoint
2. `src/services/riot_api.py` → Fetch full year matches
3. `src/agents/orchestrator.py` → Coordinate workflow
4. `src/analyzers/year_summary.py` → Aggregate statistics
5. `src/agents/year_summary_agent.py` → Generate summary
6. `src/agents/social_content_agent.py` → Create shareable content
7. Return year summary response

---

## Dependencies Between Modules

```
src/api/main.py
  ├── config.settings
  ├── src.services.riot_api
  ├── src.services.aws_bedrock
  ├── src.services.aws_comprehend
  ├── src.analyzers.match_analyzer
  ├── src.analyzers.year_summary
  ├── src.generators.visualizations
  ├── src.generators.social_content
  └── src.agents.orchestrator
        ├── src.agents.context_manager
        ├── src.agents.registry
        └── src.agents.* (all agent classes)
```

---

_Generated using BMAD Method `document-project` workflow_

