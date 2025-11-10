# API Contracts

**Last Updated:** 2025-01-27

## Overview

Rift Rewind exposes a REST API built with FastAPI. All endpoints are prefixed with `/api` (except root and health check). The API provides endpoints for player insights, match analysis, year summaries, player comparisons, and social content generation.

**Base URL:** `http://localhost:8000` (development)  
**API Documentation:** `http://localhost:8000/docs` (Swagger UI)

## Authentication

Currently, the API does not require authentication. In production, API keys or OAuth should be implemented.

## Rate Limiting

The Riot Games API integration includes rate limiting (1.2 seconds between requests). The API respects Riot's rate limits of 100 requests per 2 minutes.

## Endpoints

### Root Endpoint

#### `GET /`

Serves the static HTML frontend or returns API information.

**Response:**
```json
{
  "message": "Rift Rewind API",
  "version": "1.0.0",
  "status": "operational",
  "ui": "Visit /static/index.html for the web interface"
}
```

---

### Health Check

#### `GET /health`

Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### Player Insights

#### `GET /api/player/{summoner_name}/insights`

Get personalized insights for a player based on their recent match history.

**Path Parameters:**
- `summoner_name` (string, required): Player's Riot ID (format: `gameName#tagLine` or just `gameName`)

**Query Parameters:**
- `region` (string, default: `"na1"`): League region code
  - Valid values: `na1`, `euw1`, `eun1`, `kr`, `br1`, `la1`, `la2`, `oc1`, `ru`, `tr1`, `jp1`
- `match_count` (integer, default: `50`, min: 1, max: 100): Number of matches to analyze

**Response Model:** `PlayerInsightsResponse`

```json
{
  "strengths": ["string"],
  "weaknesses": ["string"],
  "trends": "string",
  "unexpected_insights": ["string"],
  "recommendations": ["string"],
  "key_metrics": {
    "kda": 2.5,
    "win_rate": 55.0,
    "avg_damage": 25000,
    "avg_vision_score": 45
  },
  "rank_info": {
    "tier": "Gold",
    "rank": "II",
    "lp": 1250
  },
  "visualizations": {
    "win_rate_chart": "base64_encoded_image",
    "kda_trends": "base64_encoded_image"
  }
}
```

**Example Request:**
```bash
curl "http://localhost:8000/api/player/SummonerName#NA1/insights?region=na1&match_count=50"
```

**Status Codes:**
- `200`: Success
- `404`: Summoner not found
- `500`: Internal server error or agent workflow failure

---

### Year Summary

#### `GET /api/player/{summoner_name}/year-summary`

Get comprehensive year-end summary for a player.

**Path Parameters:**
- `summoner_name` (string, required): Player's Riot ID

**Query Parameters:**
- `year` (integer, default: `2024`, min: 2020, max: 2025): Year to analyze
- `region` (string, default: `"na1"`): League region code

**Response Model:** `YearSummaryResponse`

```json
{
  "year": 2024,
  "summary": {
    "total_matches": 500,
    "total_wins": 275,
    "total_losses": 225,
    "win_rate": 55.0
  },
  "highlights": [
    {
      "type": "achievement",
      "description": "10-game win streak",
      "date": "2024-06-15"
    }
  ],
  "strengths": ["string"],
  "weaknesses": ["string"],
  "growth_areas": ["string"],
  "ai_generated_summary": "string",
  "shareable_content": {
    "year_end_card": "base64_encoded_image",
    "twitter_thread": "string",
    "achievement_post": "string"
  }
}
```

**Example Request:**
```bash
curl "http://localhost:8000/api/player/SummonerName#NA1/year-summary?year=2024&region=na1"
```

**Status Codes:**
- `200`: Success
- `404`: Summoner not found
- `500`: Internal server error

---

### Match Analysis

#### `GET /api/match/{match_id}/analysis`

Get detailed AI-generated analysis for a specific match.

**Path Parameters:**
- `match_id` (string, required): Riot Games match ID

**Query Parameters:**
- `puuid` (string, required): Player's PUUID

**Response Model:** `MatchAnalysisResponse`

```json
{
  "match_id": "NA1_1234567890",
  "analysis": "Detailed AI-generated match analysis...",
  "key_moments": [
    "Early game: Strong laning phase with 3 kills before 10 minutes",
    "Mid game: Excellent objective control..."
  ],
  "recommendations": [
    "Focus on vision control in mid game",
    "Improve CS consistency"
  ]
}
```

**Example Request:**
```bash
curl "http://localhost:8000/api/match/NA1_1234567890/analysis?puuid=player-puuid-here"
```

**Status Codes:**
- `200`: Success
- `404`: Match or player not found in match
- `500`: Internal server error

---

### Player Comparison

#### `GET /api/player/{summoner_name}/compare`

Compare two players' performance.

**Path Parameters:**
- `summoner_name` (string, required): First player's Riot ID

**Query Parameters:**
- `friend_name` (string, required): Second player's Riot ID
- `region` (string, default: `"na1"`): League region code

**Response:**
```json
{
  "player1": {
    "name": "SummonerName1",
    "stats": {
      "win_rate": 55.0,
      "avg_kda": 2.5,
      "avg_damage": 25000
    }
  },
  "player2": {
    "name": "SummonerName2",
    "stats": {
      "win_rate": 52.0,
      "avg_kda": 2.3,
      "avg_damage": 23000
    }
  },
  "comparison": "AI-generated comparison text...",
  "shareable_content": "Formatted comparison for social media..."
}
```

**Example Request:**
```bash
curl "http://localhost:8000/api/player/Player1#NA1/compare?friend_name=Player2#NA1&region=na1"
```

**Status Codes:**
- `200`: Success
- `404`: One or both summoners not found
- `500`: Internal server error

---

### Social Content

#### `GET /api/player/{summoner_name}/social-content`

Get shareable social media content for a player.

**Path Parameters:**
- `summoner_name` (string, required): Player's Riot ID

**Query Parameters:**
- `content_type` (string, default: `"year-end"`): Type of content
  - Valid values: `year-end`, `insights`, `achievements`
- `region` (string, default: `"na1"`): League region code

**Response:**
```json
{
  "year_end_card": "base64_encoded_image",
  "twitter_thread": "Formatted Twitter thread...",
  "achievement_post": "Formatted achievement post...",
  "instagram_caption": "Formatted Instagram caption..."
}
```

**Example Request:**
```bash
curl "http://localhost:8000/api/player/SummonerName#NA1/social-content?content_type=year-end&region=na1"
```

**Status Codes:**
- `200`: Success
- `400`: Invalid content type
- `404`: Summoner not found
- `500`: Internal server error

---

## Error Responses

All endpoints may return the following error responses:

### 404 Not Found
```json
{
  "detail": "Summoner not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error message describing the issue"
}
```

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

## Data Models

### PlayerInsightsResponse
- `strengths`: List of identified strengths
- `weaknesses`: List of identified weaknesses
- `trends`: Text description of performance trends
- `unexpected_insights`: List of surprising patterns discovered
- `recommendations`: List of actionable recommendations
- `key_metrics`: Dictionary of key performance metrics
- `rank_info`: Optional rank information
- `visualizations`: Optional visualization data (base64 encoded images)

### YearSummaryResponse
- `year`: Year analyzed
- `summary`: Dictionary of summary statistics
- `highlights`: List of highlight objects
- `strengths`: List of strengths
- `weaknesses`: List of weaknesses
- `growth_areas`: List of areas for improvement
- `ai_generated_summary`: AI-generated narrative summary
- `shareable_content`: Dictionary of formatted social media content

### MatchAnalysisResponse
- `match_id`: Riot Games match ID
- `analysis`: Detailed match analysis text
- `key_moments`: List of important moments in the match
- `recommendations`: List of recommendations based on match

---

_Generated using BMAD Method `document-project` workflow_

