# Setting Up Angular Frontend

This guide will help you set up and run the Angular frontend for Rift Rewind.

## Prerequisites

1. **Node.js and npm**: Install Node.js (v18 or higher) from [nodejs.org](https://nodejs.org/)
2. **Angular CLI**: Install globally with `npm install -g @angular/cli`

## Setup Steps

### 1. Install Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install npm dependencies
npm install
```

### 2. Development Mode

To run the Angular app in development mode (with hot reload):

```bash
# Navigate to frontend directory
cd frontend

# Start development server (runs on http://localhost:4200)
npm start

# Or use Angular CLI directly
ng serve
```

The app will be available at `http://localhost:4200` and will proxy API requests to your FastAPI backend.

### 3. Build for Production

To build the Angular app for production (served by FastAPI):

```bash
# Navigate to frontend directory
cd frontend

# Build Angular app (outputs to ../static/angular/)
npm run build

# The built app will be served by FastAPI at http://localhost:8000
```

### 4. Running with FastAPI Backend

1. **Build the Angular app first**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Start the FastAPI backend**:
   ```bash
   python main.py
   # Or
   uvicorn src.api.main:app --reload
   ```

3. **Access the app**: Open `http://localhost:8000` in your browser

## Project Structure

```
rift-rewind/
├── frontend/                 # Angular application
│   ├── src/
│   │   ├── app/             # Angular components
│   │   ├── styles.css       # Global styles (Hall of Legends theme)
│   │   └── main.ts          # App bootstrap
│   ├── angular.json         # Angular configuration
│   ├── package.json         # npm dependencies
│   └── tsconfig.json        # TypeScript configuration
├── static/
│   └── angular/             # Built Angular app (generated after build)
└── ...
```

## Features

- **Hall of Legends Styling**: Dark, epic theme with metallic accents
- **Responsive Design**: Works on desktop and mobile devices
- **API Integration**: Connects to FastAPI backend
- **Player Insights**: View player statistics and insights
- **Year Summary**: Get year-end summaries
- **Social Content**: Generate shareable content

## Troubleshooting

### Port Already in Use

If port 4200 is already in use:
```bash
ng serve --port 4201
```

### Build Errors

If you encounter build errors:
1. Navigate to frontend directory: `cd frontend`
2. Make sure all dependencies are installed: `npm install`
3. Clear node_modules and reinstall: `rm -rf node_modules && npm install` (or on Windows: `Remove-Item -Recurse -Force node_modules; npm install`)
4. Check Node.js version: `node --version` (should be v18+)

### API Connection Issues

If the app can't connect to the API:
1. Make sure FastAPI backend is running
2. Check CORS settings in `src/api/main.py`
3. Verify API base URL in `frontend/src/app/api.service.ts`

## Development Tips

- Use `npm run watch` to automatically rebuild on file changes
- Angular dev server supports hot reload for faster development
- Check browser console for errors and API responses
- Use Angular DevTools browser extension for debugging

## Next Steps

1. Customize the styling in `frontend/src/styles.css`
2. Add new components in `frontend/src/app/`
3. Modify API service in `frontend/src/app/api.service.ts`
4. Update components in `frontend/src/app/player-insights/`

