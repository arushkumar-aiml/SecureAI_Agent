start cmd /k "cd backend && uvicorn main:app --reload"
timeout /t 3
start cmd /k "cd frontend && streamlit run app.py"