# How to Run the App

## Quick Start (Step-by-Step)

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Environment File
Create a file named `.env` in the root directory with your credentials:

```env
RIOT_API_KEY=your_riot_api_key_here
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
BEDROCK_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-v2
APP_ENV=development
APP_DEBUG=true
API_PORT=8000
```

### 3. Run the Application
```bash
python main.py
```

### 4. Open in Browser
Once the server is running, open your browser and go to:

**API Documentation (Interactive):**
- http://localhost:8000/docs

**Alternative API Documentation:**
- http://localhost:8000/redoc

**Health Check:**
- http://localhost:8000/health

## Using the API

### Test the API
```bash
# Health check
curl http://localhost:8000/health

# Get player insights (replace YourSummonerName with actual summoner name)
curl "http://localhost:8000/api/player/YourSummonerName/insights?region=na1"
```

### Example: Get Year-End Summary
```bash
curl "http://localhost:8000/api/player/YourSummonerName/year-summary?year=2024&region=na1"
```

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, change it in `.env`:
```env
API_PORT=8001
```

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### Environment Variables Not Loading
Make sure the `.env` file is in the root directory (same folder as `main.py`)

### AWS Credentials
Make sure your AWS credentials have access to:
- Amazon Bedrock
- Amazon Comprehend

## Windows Users

If you're on Windows, you can run:
```powershell
python main.py
```

Or use the interactive API docs at:
http://localhost:8000/docs

