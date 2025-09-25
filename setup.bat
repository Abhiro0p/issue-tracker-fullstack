@echo off
echo 🚀 Setting up Issue Tracker System...

REM Check prerequisites
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed. Aborting.
    exit /b 1
)

node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is required but not installed. Aborting.
    exit /b 1
)

npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm is required but not installed. Aborting.
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Setup backend
echo 📦 Setting up backend...
cd backend

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Copy environment file
if not exist .env (
    copy .env.example .env
    echo ✅ Created .env file from template
)

cd ..

REM Setup frontend
echo 🎨 Setting up frontend...
cd frontend

REM Install dependencies
npm install

REM Check if Angular CLI is installed
ng version >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing Angular CLI globally...
    npm install -g @angular/cli
)

cd ..

echo ✅ Setup complete!
echo.
echo 🚀 To start the application:
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   venv\Scripts\activate
echo   uvicorn app.main:app --reload --port 8000
echo.
echo Terminal 2 (Frontend):
echo   cd frontend
echo   ng serve --port 4200
echo.
echo 📱 Access the application:
echo   Frontend: http://localhost:4200
echo   Backend API: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
echo 🐳 Or use Docker:
echo   docker-compose up --build
