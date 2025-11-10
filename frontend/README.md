# Rift Rewind - Angular Frontend

Angular application for the Rift Rewind League of Legends coaching agent with Hall of Legends styling.

## Prerequisites

- Node.js (v18 or higher)
- npm (v9 or higher)
- Angular CLI: `npm install -g @angular/cli`

## Installation

```bash
# Install dependencies
npm install
```

## Development

```bash
# Start development server (runs on http://localhost:4200)
ng serve

# Or use npm script
npm start
```

## Building for Production

```bash
# Build Angular app (outputs to ../static/angular/)
npm run build

# Build with watch mode
npm run watch
```

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── app.component.ts          # Main app component with navbar
│   │   ├── player-insights/          # Player insights component
│   │   └── api.service.ts            # API service for backend calls
│   ├── styles.css                    # Global styles (Hall of Legends theme)
│   └── main.ts                       # App bootstrap
├── angular.json                      # Angular configuration
└── tsconfig.json                     # TypeScript configuration
```

## Styling

The app uses a dark, epic "Hall of Legends" theme with:
- Dark backgrounds with metallic accents
- Silver, bronze, and gold color palette
- Dramatic lighting effects
- Large, bold typography
- Epic fantasy aesthetic

## API Integration

The app connects to the FastAPI backend running on the same origin. Update `api.service.ts` if you need to change the API base URL.

## Deployment

After building, the Angular app will be served by the FastAPI backend from `/static/angular/`. Make sure to run `npm run build` before deploying.

