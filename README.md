# 🏠 House Price Prediction System

A full-stack **house price prediction web application** that uses **Machine Learning** to estimate house prices based on input features.  
The system is built with **Django** and **scikit-learn** on the backend, **Celery + Redis** for background tasks, and **React** for the frontend.

---

##  Features

- Predict house prices using a trained ML model  
- Model training and retraining using **scikit-learn**  
- Asynchronous background tasks with **Celery**  
- Task queue and broker powered by **Redis**  
- REST API built with **Django**  
- Modern frontend using **React**  
- Scheduled or manual model retraining  
- Clean separation between ML logic, backend, and frontend  

---

## Tech Stack

### Backend
- **Django** – Web framework & REST API  
- **scikit-learn** – Machine learning model  
- **Celery** – Background task processing  
- **Redis** – Message broker for Celery  

### Frontend
- **React** – User interface    


---

## 🚀 How to Run the Project (Windows)

Follow these steps exactly to get everything running on your machine.

### 1. Prerequisites
- **Python 3.10+** (Make sure it's in your PATH)
- **Node.js & npm** (For the frontend)
- **Redis** (Required for Celery). 
    - On Windows, the easiest way to run Redis is via **Docker** (`docker run -p 6379:6379 redis`) or by downloading **Redis-for-Windows** (v5.0.14) from GitHub.

### 2. Setup Backend (Django)
Open a terminal in `backend/house_price_project`:
```powershell
# 1. Create a virtual environment
python -m venv venv

# 2. Activate it
.\venv\Scripts\activate
# OR if using Git Bash: source venv/Scripts/activate

# 3. Install dependencies
pip install -r ..\requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Start the server
python manage.py runserver
```

### 3. Setup Background Workers (Celery)
You need **two** more terminals (with the virtualenv activated) for Celery:

**Terminal 2 (Worker):**
```powershell
python -m celery -A house_price_project worker --loglevel=info -P solo
```

**Terminal 3 (Beat - Scheduler):**
```powershell
python -m celery -A house_price_project beat --loglevel=info
```

### 4. Setup Frontend (React)
Open a terminal in the `frontend` directory:
```powershell
# 1. Install dependencies
npm install

# 2. Start the development server
npm run dev
```
The app will be available at `http://localhost:5173`.

---

## 🏗️ Architectural Overview
- **Frontend**: React + Vite (Typescript)
- **Backend**: Django REST API
- **ML**: Scikit-Learn (Linear Regression with StandardScaler)
- **Task Queue**: Celery with Redis (Broker)
