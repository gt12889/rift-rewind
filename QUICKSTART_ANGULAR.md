# Quick Start Guide - Angular Frontend

## Prerequisites

- Node.js v18+ and npm
- Python 3.8+ with FastAPI backend running

## Setup Steps

### 1. Install Dependencies

```bash
npm install
```

### 2. Build Angular App

```bash
npm run build
```

This will build the Angular app and output it to `static/angular/`.

### 3. Start FastAPI Backend

```bash
python main.py
# Or
uvicorn src.api.main:app --reload
```

### 4. Access the App

Open your browser and navigate to:
- `http://localhost:8000` - Angular app (if built)
- `http://localhost:8000/static/index.html` - Legacy UI (fallback)

## Development Mode

For development with hot reload:

```bash
# Terminal 1: Start Angular dev server
npm start
# App will be at http://localhost:4200

# Terminal 2: Start FastAPI backend
python main.py
# API will be at http://localhost:8000
```

**Note**: In development mode, you'll need to update `api.service.ts` to point to `http://localhost:8000` for API calls.

## Features

- **Hall of Legends Styling**: Dark, epic theme with metallic accents
- **Responsive Design**: Works on all screen sizes
- **Player Insights**: View detailed player statistics
- **Year Summary**: Get comprehensive year-end summaries
- **Social Content**: Generate shareable content

## Troubleshooting

### Build Errors

If you get build errors:
1. Make sure Node.js v18+ is installed
2. Run `npm install` to install dependencies
3. Clear cache: `rm -rf node_modules package-lock.json && npm install`

### API Connection Issues

If the app can't connect to the API:
1. Make sure FastAPI backend is running
2. Check CORS settings in `src/api/main.py`
3. Verify the API base URL in `frontend/src/app/api.service.ts`

### Angular App Not Showing

If you see "Angular app not found":
1. Make sure you ran `npm run build`
2. Check that `static/angular/index.html` exists
3. Verify the build output in `static/angular/`

## Next Steps

- Customize styling in `frontend/src/styles.css`
- Add new components in `frontend/src/app/`
- Modify API service in `frontend/src/app/api.service.ts`

