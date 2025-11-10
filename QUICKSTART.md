# Quick Start Guide

## Prerequisites

- Python 3.11+
- AWS Account with Bedrock and Comprehend access
- Riot Games API Key

## 5-Minute Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   Create a `.env` file:
   ```env
   RIOT_API_KEY=your_riot_api_key
   AWS_ACCESS_KEY_ID=your_aws_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret
   AWS_REGION=us-east-1
   BEDROCK_REGION=us-east-1
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Test the API**
   ```bash
   curl http://localhost:8000/health
   ```

5. **Get player insights**
   ```bash
   curl "http://localhost:8000/api/player/YourSummonerName/insights?region=na1"
   ```

## Example API Calls

### Get Year-End Summary
```bash
curl "http://localhost:8000/api/player/YourSummonerName/year-summary?year=2024&region=na1"
```

### Compare Players
```bash
curl "http://localhost:8000/api/player/Player1/compare?friend_name=Player2&region=na1"
```

### Get Social Content
```bash
curl "http://localhost:8000/api/player/YourSummonerName/social-content?content_type=year-end&region=na1"
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Next Steps

- See `SETUP.md` for detailed setup instructions
- See `ARCHITECTURE.md` for system architecture
- See `README.md` for full documentation

