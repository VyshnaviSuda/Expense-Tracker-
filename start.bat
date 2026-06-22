@echo off
echo Starting Expense Tracker...
cd /d C:\Users\VYSHNAVI\OneDrive\Desktop\expense-tracker
start cmd /k python -m uvicorn main:app --reload
timeout /t 3
start http://127.0.0.1:8000