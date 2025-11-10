# Development Guide

**Last Updated:** 2025-01-27

## Prerequisites

### Required Software

- **Python 3.11 or higher**: [Download Python](https://www.python.org/downloads/)
- **pip**: Python package manager (included with Python)
- **Git**: Version control system
- **AWS Account**: For Bedrock and Comprehend access
- **Riot Games API Key**: [Get API Key](https://developer.riotgames.com/)

### AWS Services Access

- **Amazon Bedrock**: Access to Claude v2 model
- **Amazon Comprehend**: For NLP analysis
- **AWS IAM**: For credential management

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd rift-rewind
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
# Riot Games API
RIOT_API_KEY=your_riot_api_key_here
RIOT_API_BASE_URL=https://americas.api.riotgames.com

# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key

# AWS Bedrock
BEDROCK_MODEL_ID=anthropic.claude-v2
BEDROCK_REGION=us-east-1

# Application
APP_ENV=development
APP_DEBUG=True
API_PORT=8000

# Resource Tagging
RESOURCE_TAG_KEY=rift-rewind-hackathon
RESOURCE_TAG_VALUE=2025
```

**Note:** Never commit the `.env` file to version control. It's already in `.gitignore`.

## Running the Application

### Development Mode

```bash
python main.py
```

This starts the FastAPI server with auto-reload enabled on `http://localhost:8000`.

### Using Uvicorn Directly

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode

Set `APP_DEBUG=False` in `.env` and run:

```bash
python main.py
```

Or use uvicorn without reload:

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## Testing

### Run All Tests

```bash
pytest tests/
```

### Run Specific Test File

```bash
pytest tests/test_api.py
pytest tests/test_agents.py
```

### Run with Coverage

```bash
pytest --cov=src tests/
```

## Development Workflow

### Project Structure

```
src/
├── api/          # API endpoints
├── services/     # External service integrations
├── agents/       # Multi-agent system
├── analyzers/    # Data analysis
└── generators/   # Content generation
```

### Adding a New Endpoint

1. Open `src/api/main.py`
2. Add route handler function with decorator:
   ```python
   @app.get("/api/new-endpoint")
   async def new_endpoint():
       # Implementation
   ```
3. Add request/response models if needed
4. Update API documentation

### Adding a New Agent

1. Create agent class in `src/agents/`:
   ```python
   from src.agents.base_agent import BaseAgent
   
   class NewAgent(BaseAgent):
       def handle_request(self, request):
           # Implementation
   ```

2. Register agent in `src/api/main.py`:
   ```python
   agent_registry.register(NewAgent(context_manager))
   ```

3. Use agent via orchestrator:
   ```python
   orchestrator.delegate("new_agent", "task_name", input_data)
   ```

### Adding a New Service

1. Create service class in `src/services/`:
   ```python
   class NewService:
       def __init__(self):
           # Initialize
       
       def method(self):
           # Implementation
   ```

2. Initialize in `src/api/main.py`:
   ```python
   new_service = NewService()
   ```

3. Use in endpoints or agents

## Code Style

### Python Style Guide

- Follow PEP 8 style guide
- Use type hints for function parameters and return types
- Use docstrings for classes and functions
- Maximum line length: 100 characters

### Example

```python
from typing import Dict, List, Optional

def analyze_data(data: List[Dict], options: Optional[Dict] = None) -> Dict:
    """
    Analyze data and return results.
    
    Args:
        data: List of data dictionaries
        options: Optional analysis options
    
    Returns:
        Dictionary containing analysis results
    """
    # Implementation
    pass
```

## Common Development Tasks

### Testing API Endpoints

Use curl or Postman to test endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Player insights
curl "http://localhost:8000/api/player/SummonerName#NA1/insights?region=na1&match_count=50"

# Year summary
curl "http://localhost:8000/api/player/SummonerName#NA1/year-summary?year=2024&region=na1"
```

### Debugging

1. **Enable Debug Mode**: Set `APP_DEBUG=True` in `.env`
2. **Check Logs**: FastAPI logs requests and errors to console
3. **Use Swagger UI**: Test endpoints interactively at `/docs`
4. **Print Statements**: Add print statements for debugging (remove before commit)

### Environment Variables

All configuration is managed via environment variables loaded by `config/settings.py`:

- `RIOT_API_KEY`: Required for Riot Games API
- `AWS_ACCESS_KEY_ID`: Required for AWS services
- `AWS_SECRET_ACCESS_KEY`: Required for AWS services
- `APP_DEBUG`: Enable/disable debug mode
- `API_PORT`: Port for API server (default: 8000)

## Troubleshooting

### Common Issues

#### 1. Import Errors

**Problem:** `ModuleNotFoundError` when running

**Solution:**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`
- Check Python path includes project root

#### 2. AWS Credentials Error

**Problem:** `NoCredentialsError` from boto3

**Solution:**
- Set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in `.env`
- Or configure AWS CLI: `aws configure`
- Or use IAM role (for Lambda deployment)

#### 3. Riot API Rate Limiting

**Problem:** `429 Too Many Requests` from Riot API

**Solution:**
- The client includes rate limiting (1.2s delay)
- Reduce `match_count` parameter in requests
- Wait between test requests

#### 4. Bedrock Access Denied

**Problem:** `AccessDeniedException` from Bedrock

**Solution:**
- Ensure Bedrock is enabled in your AWS account
- Check IAM permissions for Bedrock access
- Verify region is correct (us-east-1)

#### 5. Port Already in Use

**Problem:** `Address already in use` error

**Solution:**
- Change `API_PORT` in `.env` to different port
- Or kill process using port 8000:
  ```bash
  # Windows
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  
  # macOS/Linux
  lsof -ti:8000 | xargs kill
  ```

## Building and Deployment

### Docker Build

```bash
docker build -t rift-rewind .
```

### Docker Run

```bash
docker run -p 8000:8000 --env-file .env rift-rewind
```

### AWS Lambda Deployment

1. Review `deploy/cloudformation.yaml`
2. Update parameters as needed
3. Deploy using AWS CLI or CloudFormation console:

```bash
aws cloudformation create-stack \
  --stack-name rift-rewind \
  --template-body file://deploy/cloudformation.yaml \
  --parameters ParameterKey=Environment,ParameterValue=production
```

Or use the deployment script:

```bash
cd deploy
./deploy.sh
```

## Development Best Practices

1. **Use Virtual Environments**: Always use a virtual environment for development
2. **Environment Variables**: Never commit `.env` file or API keys
3. **Type Hints**: Use type hints for better IDE support and documentation
4. **Error Handling**: Always handle exceptions and return appropriate HTTP status codes
5. **Logging**: Use Python logging module for production logging
6. **Testing**: Write tests for new features
7. **Documentation**: Update API documentation when adding endpoints
8. **Code Review**: Review code before committing

## Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Riot Games API**: https://developer.riotgames.com/
- **AWS Bedrock**: https://aws.amazon.com/bedrock/
- **AWS Comprehend**: https://aws.amazon.com/comprehend/
- **Pydantic**: https://docs.pydantic.dev/

---

_Generated using BMAD Method `document-project` workflow_

