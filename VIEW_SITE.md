# How to View the New Angular Site

## Quick Start (3 Steps)

### Step 1: Install Dependencies (First Time Only)

```bash
# Navigate to frontend directory
cd frontend

# Install Angular dependencies
npm install
```

This installs all Angular dependencies. You only need to do this once, or when dependencies change.

### Step 2: Build the Angular App

```bash
# Make sure you're in the frontend directory
cd frontend

# Build the Angular app
npm run build
```

This compiles the Angular app and outputs it to `../static/angular/` directory (relative to frontend).

**Note**: You need to rebuild every time you make changes to the Angular code.

### Step 3: Start the FastAPI Backend

```bash
python main.py
```

Or if you prefer uvicorn directly:

```bash
uvicorn src.api.main:app --reload
```

### Step 4: Open in Browser

Open your web browser and navigate to:

```
http://localhost:8000
```

You should see the new **Hall of Legends** styled Angular application!

---

## Development Mode (With Hot Reload)

If you want to develop and see changes instantly:

### Terminal 1: Angular Dev Server
```bash
# Navigate to frontend directory
cd frontend

# Start Angular dev server
npm start
```
This starts Angular dev server on `http://localhost:4200` with hot reload.

### Terminal 2: FastAPI Backend
```bash
# From project root
python main.py
```
This starts the API backend on `http://localhost:8000`.

**Note**: In dev mode, you'll access the Angular app at `http://localhost:4200`, and it will make API calls to `http://localhost:8000`.

---

## Troubleshooting

### "Angular app not found" Message

If you see this message, it means the Angular app hasn't been built yet:

1. Navigate to frontend directory: `cd frontend`
2. Make sure you ran `npm run build`
3. Check that `static/angular/browser/index.html` exists (Angular 17+ outputs to browser subdirectory)
4. Verify the build completed successfully

### Port Already in Use

If port 8000 is already in use:

```bash
# Find what's using the port (Windows PowerShell)
netstat -ano | findstr :8000

# Or change the port in config/settings.py
```

### Build Errors

If you get build errors:

```bash
# Navigate to frontend directory
cd frontend

# Clear and reinstall (Linux/Mac)
rm -rf node_modules package-lock.json
npm install
npm run build

# Or on Windows PowerShell
Remove-Item -Recurse -Force node_modules,package-lock.json
npm install
npm run build
```

### Can't See the New Design

1. Navigate to frontend directory: `cd frontend`
2. Make sure you built the Angular app: `npm run build`
3. Hard refresh your browser: `Ctrl+F5` (Windows) or `Cmd+Shift+R` (Mac)
4. Clear browser cache if needed

---

## What You Should See

The new site features:

- **Dark, epic theme** with metallic accents
- **Navigation bar** at the top (Riot Games style)
- **Hero section** with "HALL of LEGENDS" title
- **Input form** to enter Riot ID and get insights
- **Results tabs** showing player statistics

---

## File Locations

- **Angular source code**: `frontend/src/`
- **Built Angular app**: `static/angular/` (created after build)
- **FastAPI backend**: `src/api/main.py`
- **Styles**: `frontend/src/styles.css`

---

## Quick Commands Reference

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# Start development server
npm start

# Development mode (hot reload)
npm start

# Start backend
python main.py
```

