@echo off
SETLOCAL EnableDelayedExpansion

echo ==========================================
echo   House Price Prediction App Launcher
echo ==========================================
echo.

:: Check for backend venv
IF NOT EXIST "backend\house_price_project\venv\Scripts\activate" (
    echo [ERROR] Virtual environment not found in backend\house_price_project\venv
    echo Please create it first: python -m venv backend\house_price_project\venv
    pause
    exit /b
)

echo [1/4] Starting Django Backend...
start "Django Backend" cmd /k "cd backend\house_price_project && venv\Scripts\activate && python manage.py runserver"

echo [2/4] Starting Celery Worker...
start "Celery Worker" cmd /k "cd backend\house_price_project && venv\Scripts\activate && python -m celery -A house_price_project worker --loglevel=info -P solo"

echo [3/4] Starting Celery Beat (Scheduler)...
start "Celery Beat" cmd /k "cd backend\house_price_project && venv\Scripts\activate && python -m celery -A house_price_project beat --loglevel=info"

echo [4/4] Starting React Frontend (Vite)...
start "React Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ==========================================
echo   All services are starting!
echo ==========================================
echo.
echo  - Django: http://localhost:8000
echo  - Frontend: http://localhost:5173
echo.
echo Close the individual terminal windows to stop the services.
pause
