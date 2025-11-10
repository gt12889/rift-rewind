# Architecture Documentation

**Last Updated:** 2025-01-27  
**Project:** Rift Rewind  
**Architecture Pattern:** Multi-Agent System with Service-Oriented Architecture

## Executive Summary

Rift Rewind is built as a stateless REST API using FastAPI, implementing a multi-agent system architecture where specialized agents handle different aspects of League of Legends match analysis. The system integrates with AWS AI services (Bedrock and Comprehend) and the Riot Games API to provide personalized coaching insights.

The architecture emphasizes:
- **Separation of Concerns**: Clear boundaries between API, services, agents, analyzers, and generators
- **Agent-Based Processing**: Specialized agents for match analysis, insights, visualization, social content, and summaries
- **Orchestration**: Central orchestrator coordinates complex multi-step workflows
- **Stateless Design**: No database layer - all data fetched from external APIs
- **Serverless Ready**: Designed for AWS Lambda deployment

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **API Framework** | FastAPI 0.104.1 | REST API with automatic OpenAPI documentation |
| **Server** | Uvicorn 0.24.0 | ASGI server for async request handling |
| **Language** | Python 3.11+ | Primary development language |
| **AI Services** | AWS Bedrock (Claude v2) | Generative AI for insights and summaries |
| **NLP** | AWS Comprehend | Sentiment analysis and key phrase extraction |
| **Data Processing** | Pandas 2.1.3, NumPy 1.26.2 | Statistical analysis and data manipulation |
| **Visualization** | Plotly 5.18.0, Matplotlib 3.8.2, Seaborn 0.13.0 | Chart generation |
| **HTTP Client** | Requests 2.31.0, aiohttp 3.9.1 | API integration |
| **Configuration** | Pydantic Settings 2.1.0 | Type-safe configuration |
| **Deployment** | AWS Lambda, API Gateway | Serverless infrastructure |

## Architecture Pattern

### Multi-Agent System

The application uses a multi-agent architecture where specialized agents handle different tasks:

1. **MatchAnalysisAgent**: Analyzes individual matches and extracts key moments
2. **InsightsAgent**: Generates personalized insights from match data
3. **VisualizationAgent**: Creates charts and visualizations
4. **SocialContentAgent**: Formats content for social media sharing
5. **YearSummaryAgent**: Generates year-end summaries
6. **ComparisonAgent**: Compares two players' performance

### Orchestrator Pattern

The `Orchestrator` class coordinates workflows by:
- Managing agent registration and lookup
- Delegating tasks to appropriate agents
- Managing shared context between agents
- Handling parallel and sequential task execution
- Publishing events for workflow tracking

### Context Management

The `ContextManager` provides shared state for agents:
- Stores intermediate results
- Enables agent-to-agent communication
- Tracks workflow progress
- Manages data flow between agents

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client (Web/Mobile)                      │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP/REST
                        │
┌───────────────────────▼─────────────────────────────────────┐
│              FastAPI Application (src/api/main.py)          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  REST Endpoints                                      │  │
│  │  - /api/player/{name}/insights                       │  │
│  │  - /api/player/{name}/year-summary                   │  │
│  │  - /api/match/{id}/analysis                          │  │
│  │  - /api/player/{name}/compare                        │  │
│  │  - /api/player/{name}/social-content                 │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────┬─────────────────────────────────────────────┘
                │
    ┌───────────┴───────────┬──────────────┬──────────────┐
    │                       │              │              │
┌───▼──────┐  ┌───────────▼──────┐  ┌─────▼──────┐  ┌───▼──────────┐
│ Riot     │  │ Orchestrator      │  │ Analyzers  │  │ Generators   │
│ API      │  │ (Multi-Agent      │  │ (Stats)    │  │ (Viz/Social) │
│ Client   │  │  Coordinator)     │  │            │  │              │
└──────────┘  └───────────┬───────┘  └────────────┘  └──────────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
      ┌───────▼──────┐      ┌────────▼────────┐
      │ AWS Bedrock  │      │ AWS Comprehend   │
      │ (Claude v2)  │      │ (NLP Analysis)   │
      └──────────────┘      └───────────────────┘
```

## Component Overview

### 1. API Layer (`src/api/main.py`)

**Responsibilities:**
- Define REST endpoints
- Request validation using Pydantic models
- Error handling and HTTP status codes
- CORS configuration
- Static file serving

**Key Components:**
- FastAPI app instance
- Request/Response models (Pydantic BaseModel)
- Endpoint route handlers
- Service initialization
- Agent system initialization

**Dependencies:**
- Services (Riot API, AWS Bedrock, AWS Comprehend)
- Analyzers (MatchAnalyzer, YearSummaryGenerator)
- Generators (VisualizationGenerator, SocialContentGenerator)
- Orchestrator (for complex workflows)

---

### 2. Service Layer (`src/services/`)

#### RiotAPIClient (`riot_api.py`)

**Responsibilities:**
- Interact with Riot Games API
- Rate limiting (1.2 seconds between requests)
- Handle regional routing
- Parse Riot ID format (gameName#tagLine)
- Fetch summoner info, match history, match details

**Key Methods:**
- `get_summoner_by_name()`: Get summoner by Riot ID
- `get_match_history()`: Fetch match IDs for a player
- `get_match_details()`: Get detailed match data
- `get_player_match_data()`: Extract player-specific data from match
- `get_full_year_matches()`: Fetch all matches for a year

#### BedrockService (`aws_bedrock.py`)

**Responsibilities:**
- Generate AI insights using Claude v2
- Format prompts for different use cases
- Parse AI responses
- Handle AWS Bedrock API calls

**Key Methods:**
- `generate_match_analysis()`: Analyze a single match
- `generate_insights()`: Generate player insights
- `generate_year_summary()`: Create year-end summary

#### ComprehendService (`aws_comprehend.py`)

**Responsibilities:**
- Sentiment analysis of generated content
- Key phrase extraction
- Text analysis for insights

**Key Methods:**
- `analyze_match_commentary()`: Analyze match analysis text
- `extract_key_phrases()`: Extract important phrases

---

### 3. Agent System (`src/agents/`)

#### Orchestrator (`orchestrator.py`)

**Responsibilities:**
- Coordinate multi-agent workflows
- Delegate tasks to appropriate agents
- Manage parallel and sequential execution
- Handle workflow state

**Key Methods:**
- `delegate()`: Delegate task to specific agent
- `execute_workflow()`: Execute sequential workflow
- `execute_parallel()`: Execute tasks in parallel
- `get_player_insights_workflow()`: Player insights workflow
- `get_year_summary_workflow()`: Year summary workflow
- `get_comparison_workflow()`: Player comparison workflow

#### ContextManager (`context_manager.py`)

**Responsibilities:**
- Store shared context between agents
- Enable agent-to-agent communication
- Track workflow state
- Manage data flow

**Key Methods:**
- `set()`: Store value in context
- `get()`: Retrieve value from context
- `has()`: Check if key exists
- `clear()`: Clear context

#### Agent Registry (`registry.py`)

**Responsibilities:**
- Register agents by name
- Lookup agents for delegation
- Manage agent lifecycle

**Key Methods:**
- `register()`: Register an agent
- `get()`: Get agent by name
- `list_agents()`: List all registered agents

#### Base Agent (`base_agent.py`)

**Responsibilities:**
- Define agent interface
- Provide common functionality
- Handle request/response pattern

**Key Methods:**
- `handle_request()`: Process agent request
- `validate_input()`: Validate input data

#### Specialized Agents

Each agent handles a specific domain:

- **MatchAnalysisAgent**: Analyzes matches, extracts key moments
- **InsightsAgent**: Generates personalized insights
- **VisualizationAgent**: Creates charts and visualizations
- **SocialContentAgent**: Formats social media content
- **YearSummaryAgent**: Generates year-end summaries
- **ComparisonAgent**: Compares player performance

---

### 4. Analysis Layer (`src/analyzers/`)

#### MatchAnalyzer (`match_analyzer.py`)

**Responsibilities:**
- Statistical analysis of match data
- Calculate KDA, win rate, damage, vision scores
- Analyze champion and role performance
- Identify trends over time
- Detect strengths, weaknesses, and achievements

**Key Methods:**
- `analyze_player_matches()`: Comprehensive match analysis
- `_calculate_win_rate()`: Calculate win rate
- `_analyze_champions()`: Champion performance analysis
- `_analyze_roles()`: Role performance analysis
- `_analyze_trends()`: Performance trend detection
- `_identify_strengths()`: Identify player strengths
- `_identify_weaknesses()`: Identify areas for improvement

#### YearSummaryGenerator (`year_summary.py`)

**Responsibilities:**
- Aggregate year-long statistics
- Identify highlights and achievements
- Generate growth area recommendations
- Create summary statistics

**Key Methods:**
- `generate_summary()`: Generate year-end summary
- `_aggregate_statistics()`: Aggregate match statistics
- `_identify_highlights()`: Find notable achievements

---

### 5. Generation Layer (`src/generators/`)

#### VisualizationGenerator (`visualizations.py`)

**Responsibilities:**
- Create interactive charts using Plotly
- Generate static charts using Matplotlib/Seaborn
- Encode charts as base64 for API responses
- Create win rate trends, KDA trends, champion performance charts

**Key Methods:**
- `generate_win_rate_chart()`: Win rate over time
- `generate_kda_trends()`: KDA trend visualization
- `generate_champion_performance()`: Champion comparison charts

#### SocialContentGenerator (`social_content.py`)

**Responsibilities:**
- Format content for social media platforms
- Generate year-end cards
- Create Twitter threads
- Format achievement posts

**Key Methods:**
- `generate_year_end_card()`: Year-end summary card
- `generate_twitter_thread()`: Formatted Twitter thread
- `generate_achievement_post()`: Achievement announcement

---

## Data Flow

### Player Insights Workflow

1. **API Request** → `GET /api/player/{name}/insights`
2. **Riot API** → Fetch summoner info and match history
3. **Orchestrator** → Start `get_player_insights_workflow()`
4. **MatchAnalysisAgent** → Analyze matches, extract statistics
5. **InsightsAgent** → Generate personalized insights using Bedrock
6. **VisualizationAgent** → Create charts and visualizations
7. **Response** → Return combined insights with visualizations

### Year Summary Workflow

1. **API Request** → `GET /api/player/{name}/year-summary`
2. **Riot API** → Fetch full year matches
3. **Orchestrator** → Start `get_year_summary_workflow()`
4. **YearSummaryGenerator** → Aggregate statistics
5. **YearSummaryAgent** → Generate AI summary using Bedrock
6. **SocialContentAgent** → Create shareable content
7. **Response** → Return year summary with social content

### Match Analysis Workflow

1. **API Request** → `GET /api/match/{id}/analysis`
2. **Riot API** → Fetch match details
3. **BedrockService** → Generate AI analysis
4. **ComprehendService** → Analyze sentiment and extract key phrases
5. **Response** → Return match analysis with key moments

---

## AWS Services Integration

### Amazon Bedrock

**Purpose:** Generative AI for personalized content

**Usage:**
- Player insights generation
- Year-end summaries
- Match analysis
- Social comparisons

**Model:** Anthropic Claude v2

**Integration:** `src/services/aws_bedrock.py`

### Amazon Comprehend

**Purpose:** Natural language processing

**Usage:**
- Sentiment analysis of generated content
- Key phrase extraction
- Content analysis

**Integration:** `src/services/aws_comprehend.py`

### AWS Lambda (Deployment)

**Purpose:** Serverless compute

**Configuration:** `deploy/cloudformation.yaml`

**Features:**
- Automatic scaling
- Pay-per-use pricing
- API Gateway integration

---

## Security Considerations

- **API Keys**: Stored in environment variables (not committed)
- **AWS Credentials**: Via IAM roles in production (Lambda execution role)
- **Rate Limiting**: Implemented for Riot API calls (1.2s delay)
- **Input Validation**: Pydantic models validate all inputs
- **CORS**: Configured for web access (currently allows all origins)

## Performance Optimizations

- **Rate Limiting**: Respects Riot API rate limits
- **Async Processing**: FastAPI async endpoints for concurrent requests
- **Parallel Agent Execution**: Orchestrator supports parallel task execution
- **Efficient Data Structures**: Pandas DataFrames for statistical analysis
- **Caching**: Consider implementing caching for frequently accessed data

## Scalability

- **Stateless Design**: No database means horizontal scaling is straightforward
- **Serverless Architecture**: Lambda provides automatic scaling
- **API Gateway**: Handles request routing and scaling
- **Resource Tagging**: All AWS resources tagged for cost tracking

## Testing Strategy

- **Unit Tests**: `tests/test_agents.py`, `tests/test_api.py`
- **Integration Tests**: Test API endpoints with mock services
- **Agent Tests**: Test individual agent functionality
- **Workflow Tests**: Test orchestrator workflows

## Deployment Architecture

### Development
- Local FastAPI server on port 8000
- Direct AWS service access via credentials
- Hot reload enabled

### Production
- AWS Lambda function
- API Gateway for HTTP routing
- CloudFormation for infrastructure as code
- Environment variables for configuration

---

_Generated using BMAD Method `document-project` workflow_

