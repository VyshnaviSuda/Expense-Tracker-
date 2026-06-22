
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
import datetime
import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# This defines what data we expect when adding an expense
class ExpenseCreate(BaseModel):
    amount: float
    category: str
    note: str = ""
    date: datetime.date = datetime.date.today()


# Add a new expense
@app.post("/expenses")
def add_expense(expense: ExpenseCreate, db: Session = Depends(database.get_db)):
    db_expense = models.Expense(
        amount=expense.amount,
        category=expense.category,
        note=expense.note,
        date=expense.date
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

# Get all expenses
@app.get("/expenses")
def get_expenses(db: Session = Depends(database.get_db)):
    return db.query(models.Expense).all()

# Delete an expense
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(database.get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully"}
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")