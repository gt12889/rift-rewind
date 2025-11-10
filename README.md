# Rift Rewind 🎮

An AI-powered coaching agent for League of Legends players that uses AWS AI services and the Riot Games API to help players reflect, learn, and improve. Rift Rewind generates personalized end-of-year insights, identifies strengths and weaknesses, creates visualizations, and produces shareable social media content.

## 🚀 Access

**Public URL:** [Add your working application URL here]

## 📁 Code Repository

**Repository URL:** [Add your public GitHub/GitLab repository URL here]

This repository is open source and licensed under the [Apache License 2.0](https://opensource.org/licenses/Apache-2.0).

## 🎬 Demo Video

**Video URL:** [Add your YouTube/Vimeo/Facebook Video URL here]

*Note: Video should be approximately 3 minutes and demonstrate your submission.*

## 📊 Methodology

### How the Coaching Agent Works

Rift Rewind is an intelligent agent that transforms end-of-game match data into personalized, end-of-year insights that players can celebrate, learn from, and share. The system:

1. **Data Collection**: Fetches end-of-game match data from Riot Games API using the player's PUUID
2. **Data Analysis**: Processes match data to extract statistics, trends, and patterns using custom analysis algorithms
3. **AI Enhancement**: Uses AWS Bedrock (Claude) to generate personalized retrospectives, unexpected insights, and engaging summaries that spark reflection
4. **Visualization**: Creates interactive charts and graphs showing player progress over time
5. **Content Generation**: Produces shareable social media content and year-end summaries that celebrate achievements and highlight growth areas

### Approach to Analyzing Match Data

The system analyzes match data through multiple layers:

- **Statistical Analysis**: Calculates KDA, win rates, damage output, vision scores, and CS across different champions and roles
- **Trend Analysis**: Identifies performance trends over time using rolling averages and time-series analysis
- **Pattern Recognition**: Detects persistent habits, strengths, and weaknesses through comparative analysis
- **Champion & Role Analysis**: Breaks down performance by champion and role to identify specializations
- **Achievement Detection**: Identifies notable achievements like perfect KDA games, high damage games, and win streaks

### Additional Data Sources

- **Riot Games API**: Primary data source for match history, player statistics, and match details
- **AWS Bedrock**: Generative AI for creating personalized insights and engaging summaries
- **AWS Comprehend**: Sentiment analysis and key phrase extraction from match analysis text

### Key Insights & Recommendations Logic

The system generates personalized insights through a multi-step process:

1. **Statistical Computation**: Calculates key metrics (KDA, win rate, damage, vision, CS) from end-of-game match data
2. **Comparative Analysis**: Compares recent performance to historical performance to identify trends and patterns
3. **AI-Powered Analysis**: Uses AWS Bedrock to analyze statistics and generate contextual insights, including unexpected insights that spark reflection
4. **Personalization**: Tailors recommendations based on player's champion pool, role preferences, and skill level
5. **Actionable Recommendations**: Provides specific, actionable advice rather than generic tips
6. **Unexpected Insights**: Surfaces surprising patterns, correlations, and non-obvious insights that help players reflect on their gameplay habits

### Discoveries & Learnings

**Challenges Encountered:**
- Rate limiting with Riot Games API required careful request management
- Processing large match histories efficiently required optimization
- Balancing AI-generated content with statistical accuracy

**Improvements Made:**
- Implemented rate limiting and request queuing for API calls
- Added caching mechanisms for frequently accessed data
- Optimized data processing pipelines for better performance
- Enhanced visualization generation with interactive charts

**Surprising Patterns Found:**
- Players often have significant performance differences between roles
- Champion mastery correlates strongly with win rate
- Vision control is a key differentiator between skill levels
- Performance trends often show seasonal patterns
- Unexpected correlations between playtime and performance
- Hidden patterns in champion selection that reveal playstyle preferences

## 🛠️ Tooling

### AWS AI Services Used

#### Amazon Bedrock
**Role**: Primary generative AI service for creating personalized insights and retrospectives
- **Model**: Anthropic Claude v2
- **Usage**: 
  - Generates personalized insights from end-of-game match data
  - Creates engaging year-end summaries and retrospectives that players can celebrate and share
  - Surfaces unexpected insights that spark reflection on gameplay habits
  - Produces match-by-match analysis and recommendations
  - Generates social comparison content between players
- **Why**: Bedrock provides powerful generative AI capabilities that transform raw statistics into meaningful, personalized narratives. It goes beyond traditional analytics by identifying surprising patterns, unexpected correlations, and insights that help players reflect on their journey and growth

#### Amazon Comprehend
**Role**: Natural language processing for sentiment analysis and key phrase extraction
- **Usage**:
  - Analyzes sentiment of match analysis text
  - Extracts key phrases and focus areas from insights
  - Identifies tone and emotional context in generated content
- **Why**: Comprehend adds an additional layer of understanding to AI-generated content, helping identify the most important insights and ensuring appropriate tone

#### AWS Lambda (via CloudFormation)
**Role**: Serverless compute for API endpoints
- **Usage**: Hosts the FastAPI application for scalable, cost-effective deployment
- **Why**: Lambda provides automatic scaling and pay-per-use pricing, ideal for hackathon projects

#### AWS API Gateway
**Role**: API management and routing
- **Usage**: Exposes REST API endpoints for the application
- **Why**: Provides secure, scalable API access with built-in rate limiting and monitoring

### Additional Technologies

- **FastAPI**: Modern Python web framework for building the REST API
- **Riot Games API**: Official League of Legends data source
- **Plotly**: Interactive visualization library for charts and graphs
- **Pandas/NumPy**: Data processing and statistical analysis
- **Boto3**: AWS SDK for Python for service integration

## 🏷️ Resource Tagging

All AWS resources are tagged with:
- **Key:** `rift-rewind-hackathon`
- **Value:** `2025`

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 👥 Contributors

[Add contributor names/contact information]

## 📧 Contact

[Add contact information if needed]
