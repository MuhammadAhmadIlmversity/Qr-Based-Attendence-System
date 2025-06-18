from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/pin", response_model=schemas.AuthResponse)
def pin_login(data: schemas.PINRequest, db: Session = Depends(get_db)):
    if crud.verify_pin(db, data.emp_id, data.pin):
        return {"success": True, "message": "PIN verified"}
    raise HTTPException(status_code=401, detail="Invalid PIN")
