from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.routes.auth import schemas, crud
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=schemas.EmployeeResponse)
def create_employee(emp: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    existing = crud.get_employee_by_id(db, emp.emp_id)
    if existing:
        raise HTTPException(status_code=400, detail="Employee already exists")
    return crud.create_employee(db, emp)

@router.get("/list", response_model=list[schemas.EmployeeResponse])
def list_employees(db: Session = Depends(get_db)):
    return crud.get_all_employees(db)
