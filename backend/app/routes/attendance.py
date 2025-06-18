from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal  # Updated import

router = APIRouter()

# Updated get_db function using SessionLocal
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/employee/{emp_id}", response_model=list[schemas.AttendanceOut])
def get_employee_logs(emp_id: str, db: Session = Depends(get_db)):
    logs = crud.get_attendance_by_employee(db, emp_id)
    if not logs:
        raise HTTPException(status_code=404, detail="No records found")
    return logs

@router.get("/all", response_model=list[schemas.AttendanceOut])
def get_all_logs(db: Session = Depends(get_db)):
    return crud.get_all_attendance(db)
