from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/map", response_model=schemas.AccessMappingResponse)
def create_mapping(mapping: schemas.AccessMappingCreate, db: Session = Depends(get_db)):
    return crud.create_access_mapping(db, mapping)

@router.get("/employee/{emp_id}", response_model=list[schemas.AccessMappingResponse])
def get_mappings_for_employee(emp_id: str, db: Session = Depends(get_db)):
    return crud.get_employee_access_doors(db, emp_id)
