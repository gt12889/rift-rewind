# Architecture Overview

## System Architecture

```
┌─────────────────┐
│   Client App    │
│  (Web/Mobile)   │
└────────┬────────┘
         │
         │ HTTP/REST
         │
┌────────▼─────────────────────────────────────┐
│         FastAPI Application                  │
│  ┌──────────────────────────────────────┐   │
│  │  API Endpoints                       │   │
│  │  - /api/player/{name}/insights       │   │
│  │  - /api/player/{name}/year-summary   │   │
│  │  - /api/match/{id}/analysis          │   │
│  │  - /api/player/{name}/compare         │   │
│  └──────────────────────────────────────┘   │
└────────┬────────────────────────────────────┘
         │
    ┌────┴────┬──────────────┬──────────────┐
    │         │              │              │
┌───▼───┐ ┌──▼──────┐ ┌──────▼──────┐ ┌─────▼─────┐
│ Riot  │ │ AWS    │ │ AWS         │ │ Match     │
│ API   │ │ Bedrock│ │ Comprehend  │ │ Analyzer  │
└───────┘ └────────┘ └─────────────┘ └───────────┘
```

## Component Overview

### 1. API Layer (`src/api/main.py`)
- FastAPI application with REST endpoints
- Request validation and error handling
- CORS configuration for web access

### 2. Service Layer (`src/services/`)

#### Riot API Client (`riot_api.py`)
- Handles all interactions with Riot Games API
- Rate limiting and request management
- Match history fetching and processing

#### AWS Bedrock Service (`aws_bedrock.py`)
- Generative AI for insights and summaries
- Prompt engineering for personalized content
- Response parsing and formatting

#### AWS Comprehend Service (`aws_comprehend.py`)
- Sentiment analysis of generated content
- Key phrase extraction
- Text analysis for insights

### 3. Analysis Layer (`src/analyzers/`)

#### Match Analyzer (`match_analyzer.py`)
- Statistical analysis of match data
- KDA, win rate, damage calculations
- Champion and role performance analysis
- Trend identification over time

#### Year Summary Generator (`year_summary.py`)
- Aggregates year-long statistics
- Identifies highlights and achievements
- Generates growth area recommendations

### 4. Generation Layer (`src/generators/`)

#### Visualization Generator (`visualizations.py`)
- Creates interactive charts using Plotly
- Win rate trends, KDA trends
- Champion and role performance charts
- Base64 encoding for API responses

#### Social Content Generator (`social_content.py`)
- Generates shareable social media content
- Year-end cards and summaries
- Twitter threads and posts
- Achievement announcements

## Data Flow

1. **Request**: Client requests player insights via API
2. **Authentication**: API validates request and extracts player name
3. **Data Fetching**: Riot API client fetches match history
4. **Analysis**: Match analyzer processes match data
5. **AI Enhancement**: Bedrock generates personalized insights
6. **Visualization**: Charts and graphs are generated
7. **Content Generation**: Social media content is created
8. **Response**: Combined results returned to client

## AWS Services Integration

### Amazon Bedrock
- **Purpose**: Generative AI for personalized content
- **Model**: Anthropic Claude v2
- **Use Cases**:
  - Player insights generation
  - Year-end summaries
  - Match analysis
  - Social comparisons

### Amazon Comprehend
- **Purpose**: Natural language processing
- **Use Cases**:
  - Sentiment analysis
  - Key phrase extraction
  - Content analysis

### AWS Lambda
- **Purpose**: Serverless compute
- **Deployment**: CloudFormation template
- **Scaling**: Automatic based on request volume

### AWS API Gateway
- **Purpose**: API management
- **Features**: Rate limiting, monitoring, security

## Security Considerations

- API keys stored in environment variables
- AWS credentials via IAM roles (production)
- Rate limiting on Riot API calls
- Input validation on all endpoints
- CORS configuration for web access

## Performance Optimizations

- Rate limiting to respect API limits
- Caching for frequently accessed data
- Batch processing for match history
- Efficient data structures for analysis
- Async processing where possible

## Scalability

- Serverless architecture (Lambda)
- Stateless API design
- Horizontal scaling via API Gateway
- Efficient data processing pipelines
- Resource tagging for cost tracking

