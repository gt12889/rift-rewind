# Setup Guide

## Prerequisites

- Python 3.11 or higher
- AWS Account with access to:
  - Amazon Bedrock
  - Amazon Comprehend
  - AWS Lambda
  - AWS API Gateway
- Riot Games API Key (get from [Riot Developer Portal](https://developer.riotgames.com/))

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rift-rewind
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```
   RIOT_API_KEY=your_riot_api_key_here
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_REGION=us-east-1
   BEDROCK_REGION=us-east-1
   ```

5. **Configure AWS Bedrock**
   - Ensure you have access to Amazon Bedrock in your AWS account
   - The default model is `anthropic.claude-v2` - ensure it's enabled in your region
   - Update `BEDROCK_MODEL_ID` in `.env` if using a different model

## Running Locally

1. **Start the development server**
   ```bash
   python main.py
   ```

2. **Access the API**
   - API will be available at `http://localhost:8000`
   - API documentation at `http://localhost:8000/docs`
   - Interactive API explorer at `http://localhost:8000/redoc`

## API Endpoints

### Get Player Insights
```
GET /api/player/{summoner_name}/insights?region=na1&match_count=50
```

### Get Year-End Summary
```
GET /api/player/{summoner_name}/year-summary?year=2024&region=na1
```

### Get Match Analysis
```
GET /api/match/{match_id}/analysis?puuid={player_puuid}
```

### Compare Players
```
GET /api/player/{summoner_name}/compare?friend_name={friend_name}&region=na1
```

### Get Social Content
```
GET /api/player/{summoner_name}/social-content?content_type=year-end&region=na1
```

## Deployment

### AWS Lambda Deployment

1. **Package the application**
   ```bash
   pip install -r requirements.txt -t .
   zip -r rift-rewind.zip . -x "*.git*" "*.env*" "*.pyc*" "__pycache__/*"
   ```

2. **Deploy using CloudFormation**
   ```bash
   cd deploy
   chmod +x deploy.sh
   ./deploy.sh production
   ```

3. **Update environment variables in Lambda**
   - Set `RIOT_API_KEY` in Lambda environment variables
   - Configure AWS credentials via IAM roles

### Environment Variables for Production

Store sensitive values in AWS Systems Manager Parameter Store or AWS Secrets Manager:

```bash
aws ssm put-parameter --name /rift-rewind/riot-api-key --value "your_key" --type SecureString
```

## Testing

```bash
# Test the API
curl http://localhost:8000/health

# Test player insights
curl http://localhost:8000/api/player/YourSummonerName/insights?region=na1
```

## Troubleshooting

### Riot API Rate Limits
- The application includes rate limiting (1.2 seconds between requests)
- For production, implement request queuing and caching

### AWS Bedrock Access
- Ensure Bedrock is enabled in your AWS account
- Check IAM permissions for Bedrock access
- Verify the model ID is correct for your region

### Common Issues
- **Import errors**: Ensure all dependencies are installed
- **API key errors**: Verify Riot API key is valid and not expired
- **AWS credential errors**: Check AWS credentials and region configuration

