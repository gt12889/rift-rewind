# Rift Rewind Documentation Index

**Type:** Monolith  
**Primary Language:** Python  
**Architecture:** Multi-Agent System with REST API  
**Last Updated:** 2025-01-27

## Project Overview

Rift Rewind is an AI-powered coaching agent for League of Legends players that transforms raw match data into personalized, actionable insights. The system uses AWS AI services (Bedrock and Comprehend) combined with the Riot Games API to help players reflect on their performance, identify growth areas, and celebrate achievements.

The application follows a multi-agent architecture where specialized agents handle different aspects of analysis (match analysis, insights generation, visualization, social content, year summaries, and player comparisons). An orchestrator coordinates these agents to execute complex workflows.

## Quick Reference

- **Tech Stack:** FastAPI, Python 3.11+, AWS Bedrock (Claude v2), AWS Comprehend, Pandas, Plotly
- **Entry Point:** `main.py` → `src/api/main.py`
- **Architecture Pattern:** Multi-Agent System with Service-Oriented Architecture
- **Database:** None (stateless API)
- **Deployment:** AWS Lambda + API Gateway

## Generated Documentation

### Core Documentation

- [Project Overview](./project-overview.md) - Executive summary and high-level architecture
- [Architecture](./architecture.md) - Detailed technical architecture
- [Source Tree Analysis](./source-tree-analysis.md) - Annotated directory structure
- [API Contracts](./api-contracts.md) - API endpoints and schemas
- [Development Guide](./development-guide.md) - Local setup and development workflow

### Optional Documentation

- [Deployment Guide](./deployment-guide.md) _(To be generated)_ - Deployment process and infrastructure

## Existing Documentation

- [README.md](../README.md) - Main project README with methodology and tooling
- [ARCHITECTURE.md](../ARCHITECTURE.md) - System architecture overview
- [PROJECT_SUMMARY.md](../PROJECT_SUMMARY.md) - Project summary and features
- [SETUP.md](../SETUP.md) - Detailed setup instructions
- [QUICKSTART.md](../QUICKSTART.md) - Quick start guide
- [RUN_APP.md](../RUN_APP.md) - Run instructions
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [FEATURES.md](../FEATURES.md) - Feature list

## Getting Started

### Prerequisites

- Python 3.11 or higher
- AWS Account with Bedrock and Comprehend access
- Riot Games API Key
- pip package manager

### Setup

```bash
# Clone repository
git clone <repository-url>
cd rift-rewind

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
cp .env.example .env
# Edit .env with your credentials
```

### Run Locally

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Run Tests

```bash
pytest tests/
```

## For AI-Assisted Development

This documentation was generated specifically to enable AI agents to understand and extend this codebase.

### When Planning New Features:

**API-only features:**
→ Reference: `architecture.md`, `api-contracts.md`

**Agent system features:**
→ Reference: `architecture.md` (Multi-Agent System section), `source-tree-analysis.md` (agents/ directory)

**Analysis features:**
→ Reference: `architecture.md` (Analysis Layer), `source-tree-analysis.md` (analyzers/ directory)

**Visualization features:**
→ Reference: `architecture.md` (Generation Layer), `source-tree-analysis.md` (generators/ directory)

**Deployment changes:**
→ Reference: `deploy/cloudformation.yaml` in project root

## Project Structure Summary

```
rift-rewind/
├── src/
│   ├── api/              # FastAPI application and endpoints
│   ├── services/         # External service integrations (Riot API, AWS)
│   ├── agents/           # Multi-agent system components
│   ├── analyzers/        # Match data analysis algorithms
│   └── generators/       # Content generation (visualizations, social)
├── config/               # Configuration and settings
├── deploy/               # Deployment scripts and CloudFormation
├── static/               # Static HTML frontend
├── tests/                # Test suite
└── docs/                 # Generated documentation (this folder)
```

## Key Components

### API Endpoints

- `GET /api/player/{name}/insights` - Get personalized player insights
- `GET /api/player/{name}/year-summary` - Get year-end summary
- `GET /api/match/{id}/analysis` - Get detailed match analysis
- `GET /api/player/{name}/compare` - Compare two players
- `GET /api/player/{name}/social-content` - Get shareable social content

### Multi-Agent System

- **Orchestrator**: Coordinates workflows and delegates to agents
- **MatchAnalysisAgent**: Analyzes matches and extracts key moments
- **InsightsAgent**: Generates personalized insights
- **VisualizationAgent**: Creates charts and visualizations
- **SocialContentAgent**: Formats social media content
- **YearSummaryAgent**: Generates year-end summaries
- **ComparisonAgent**: Compares player performance

### Services

- **RiotAPIClient**: Riot Games API integration with rate limiting
- **BedrockService**: AWS Bedrock (Claude v2) integration
- **ComprehendService**: AWS Comprehend NLP integration

### Analyzers

- **MatchAnalyzer**: Statistical analysis of match data
- **YearSummaryGenerator**: Year-end aggregation and summaries

### Generators

- **VisualizationGenerator**: Chart generation (Plotly, Matplotlib)
- **SocialContentGenerator**: Social media content formatting

## Technology Stack

| Category | Technology | Version |
|----------|-----------|---------|
| Framework | FastAPI | 0.104.1 |
| Runtime | Python | 3.11+ |
| Server | Uvicorn | 0.24.0 |
| AI | AWS Bedrock (Claude v2) | - |
| NLP | AWS Comprehend | - |
| Data Processing | Pandas | 2.1.3 |
| Visualization | Plotly | 5.18.0 |
| HTTP Client | Requests | 2.31.0 |
| Config | Pydantic Settings | 2.1.0 |
| Deployment | AWS Lambda | - |

## Architecture Highlights

- **Multi-Agent System**: Specialized agents handle different analysis tasks
- **Orchestrator Pattern**: Central coordinator manages workflows
- **Context Management**: Shared context system for agent communication
- **Event-Driven**: Event bus for agent coordination
- **Stateless API**: No database layer - all data fetched from Riot Games API
- **Serverless Ready**: Designed for AWS Lambda deployment

## Next Steps

1. Review the [Architecture](./architecture.md) document for detailed system design
2. Check [API Contracts](./api-contracts.md) for endpoint documentation
3. Follow [Development Guide](./development-guide.md) for local setup
4. Explore [Source Tree Analysis](./source-tree-analysis.md) for code organization

---

_Documentation generated by BMAD Method `document-project` workflow_

