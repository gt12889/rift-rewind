# Rift Rewind - Project Overview

**Date:** 2025-01-27
**Type:** Backend API
**Architecture:** Multi-Agent System with REST API

## Executive Summary

Rift Rewind is an AI-powered coaching agent for League of Legends players that transforms raw match data into personalized, actionable insights. The system uses AWS AI services (Bedrock and Comprehend) combined with the Riot Games API to help players reflect on their performance, identify growth areas, and celebrate achievements.

The application follows a multi-agent architecture where specialized agents handle different aspects of analysis (match analysis, insights generation, visualization, social content, year summaries, and player comparisons). An orchestrator coordinates these agents to execute complex workflows.

## Project Classification

- **Repository Type:** Monolith
- **Project Type(s):** Backend API
- **Primary Language(s):** Python
- **Architecture Pattern:** Multi-Agent System with Service-Oriented Architecture

## Technology Stack Summary

| Category | Technology | Version | Justification |
|----------|-----------|---------|---------------|
| **Framework** | FastAPI | 0.104.1 | Modern async Python web framework with automatic API documentation |
| **Runtime** | Python | 3.11+ | Primary development language |
| **Server** | Uvicorn | 0.24.0 | ASGI server for FastAPI |
| **AWS AI** | Bedrock (Claude v2) | - | Generative AI for personalized insights and summaries |
| **AWS NLP** | Comprehend | - | Sentiment analysis and key phrase extraction |
| **Data Processing** | Pandas | 2.1.3 | Statistical analysis and data manipulation |
| **Visualization** | Plotly | 5.18.0 | Interactive chart generation |
| **Visualization** | Matplotlib | 3.8.2 | Static chart generation |
| **Visualization** | Seaborn | 0.13.0 | Statistical visualization |
| **HTTP Client** | Requests | 2.31.0 | Riot Games API integration |
| **Async HTTP** | aiohttp | 3.9.1 | Async HTTP requests |
| **Config** | Pydantic Settings | 2.1.0 | Type-safe configuration management |
| **Deployment** | AWS Lambda | - | Serverless compute |
| **API Gateway** | AWS API Gateway | - | API management and routing |
| **Infrastructure** | CloudFormation | - | Infrastructure as code |

## Key Features

1. **Personalized Player Insights**: AI-powered analysis identifies strengths, weaknesses, and trends
2. **Year-End Summaries**: Comprehensive year-long statistics and highlights
3. **Match Analysis**: Detailed analysis of individual matches with key moments
4. **Player Comparisons**: Compare performance between two players
5. **Visualizations**: Interactive charts showing performance trends
6. **Social Content Generation**: Shareable year-end cards and summaries

## Architecture Highlights

- **Multi-Agent System**: Specialized agents handle different analysis tasks
- **Orchestrator Pattern**: Central coordinator manages workflows and agent delegation
- **Context Management**: Shared context system for agent communication
- **Event-Driven**: Event bus for agent coordination and workflow tracking
- **Stateless API**: No database layer - all data fetched from Riot Games API
- **Serverless Ready**: Designed for AWS Lambda deployment

## Development Overview

### Prerequisites

- Python 3.11 or higher
- AWS Account with Bedrock and Comprehend access
- Riot Games API Key
- pip package manager

### Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables (see `.env.example`)
3. Configure AWS credentials
4. Run the application: `python main.py`
5. Access API documentation: `http://localhost:8000/docs`

### Key Commands

- **Install:** `pip install -r requirements.txt`
- **Dev:** `python main.py` (runs with auto-reload)
- **Test:** `pytest tests/`
- **Deploy:** Use CloudFormation template in `deploy/` directory

## Repository Structure

```
rift-rewind/
├── src/
│   ├── api/              # FastAPI application and endpoints
│   ├── services/         # External service integrations (Riot API, AWS)
│   ├── analyzers/         # Match data analysis algorithms
│   ├── generators/        # Content generation (visualizations, social)
│   └── agents/            # Multi-agent system components
├── config/                # Configuration and settings
├── deploy/                # Deployment scripts and CloudFormation
├── static/                # Static HTML frontend
├── tests/                 # Test suite
├── docs/                   # Generated documentation
└── main.py               # Application entry point
```

## Documentation Map

For detailed information, see:

- [index.md](./index.md) - Master documentation index
- [architecture.md](./architecture.md) - Detailed architecture
- [source-tree-analysis.md](./source-tree-analysis.md) - Directory structure
- [api-contracts.md](./api-contracts.md) - API endpoints documentation
- [development-guide.md](./development-guide.md) - Development workflow

---

_Generated using BMAD Method `document-project` workflow_

