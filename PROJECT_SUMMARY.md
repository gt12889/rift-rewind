# Rift Rewind - Project Summary

## Overview

Rift Rewind is an AI-powered coaching agent for League of Legends players that transforms raw match data into personalized, actionable insights. The system uses AWS AI services (Bedrock and Comprehend) combined with the Riot Games API to help players reflect on their performance, identify growth areas, and celebrate achievements.

## Key Features

### 1. Personalized Insights
- **Strengths & Weaknesses**: AI-powered analysis identifies persistent strengths and areas for improvement
- **Trend Analysis**: Tracks performance over time to show improvement or decline
- **Champion & Role Analysis**: Breaks down performance by champion and role

### 2. Year-End Summaries
- **Comprehensive Recaps**: Full-year statistics and highlights
- **Achievement Tracking**: Identifies notable achievements and milestones
- **Growth Areas**: Suggests specific areas for improvement in the coming year

### 3. Visualizations
- **Win Rate Trends**: Interactive charts showing performance over time
- **KDA Trends**: Visual representation of combat effectiveness
- **Champion Performance**: Comparison of performance across different champions
- **Role Performance**: Analysis of effectiveness in different roles

### 4. Social Features
- **Shareable Content**: Year-end cards and summaries optimized for social media
- **Player Comparisons**: Compare performance with friends
- **Achievement Posts**: Auto-generated social media posts for achievements
- **Twitter Threads**: Formatted content ready for Twitter

### 5. Match Analysis
- **Detailed Match Insights**: AI-generated analysis for individual matches
- **Key Moments**: Identifies important moments that impacted the game
- **Actionable Recommendations**: Specific advice for improvement

## Technical Architecture

### Backend
- **FastAPI**: Modern Python web framework for REST API
- **Riot Games API**: Official League of Legends data source
- **AWS Bedrock**: Generative AI for personalized content
- **AWS Comprehend**: Natural language processing
- **AWS Lambda**: Serverless compute for scalability
- **AWS API Gateway**: API management and routing

### Data Processing
- **Statistical Analysis**: Custom algorithms for KDA, win rate, damage calculations
- **Trend Detection**: Time-series analysis for performance trends
- **Pattern Recognition**: Identifies persistent habits and patterns

### AI Integration
- **AWS Bedrock (Claude v2)**: Generates personalized insights and summaries
- **AWS Comprehend**: Analyzes sentiment and extracts key phrases
- **Prompt Engineering**: Carefully crafted prompts for relevant, actionable insights

## Project Structure

```
rift-rewind/
├── src/
│   ├── api/              # FastAPI application and endpoints
│   ├── services/         # External service integrations
│   │   ├── riot_api.py   # Riot Games API client
│   │   ├── aws_bedrock.py # AWS Bedrock integration
│   │   └── aws_comprehend.py # AWS Comprehend integration
│   ├── analyzers/        # Match data analysis
│   │   ├── match_analyzer.py # Statistical analysis
│   │   └── year_summary.py # Year-end summary generation
│   └── generators/       # Content generation
│       ├── visualizations.py # Chart generation
│       └── social_content.py # Social media content
├── config/               # Configuration
├── deploy/               # Deployment scripts
├── tests/                # Test suite
└── main.py              # Application entry point
```

## API Endpoints

### Player Insights
- `GET /api/player/{summoner_name}/insights` - Get personalized insights
- `GET /api/player/{summoner_name}/year-summary` - Get year-end summary
- `GET /api/player/{summoner_name}/compare` - Compare with friend
- `GET /api/player/{summoner_name}/social-content` - Get shareable content

### Match Analysis
- `GET /api/match/{match_id}/analysis` - Get detailed match analysis

## AWS Services Used

1. **Amazon Bedrock**: Generative AI for insights and summaries
2. **Amazon Comprehend**: Sentiment analysis and key phrase extraction
3. **AWS Lambda**: Serverless compute
4. **AWS API Gateway**: API management
5. **AWS CloudFormation**: Infrastructure as code

## Resource Tagging

All AWS resources are tagged with:
- **Key**: `rift-rewind-hackathon`
- **Value**: `2025`

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables (see `.env.example`)
3. Run the application: `python main.py`
4. Access API documentation: `http://localhost:8000/docs`

## Documentation

- **README.md**: Full project documentation
- **SETUP.md**: Detailed setup instructions
- **ARCHITECTURE.md**: System architecture overview
- **QUICKSTART.md**: Quick start guide
- **CONTRIBUTING.md**: Contribution guidelines

## License

Apache License 2.0 - See LICENSE file for details.

