from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=schemas.DeviceResponse)
def create_device(
    device: schemas.DeviceCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    existing = db.query(models.Device).filter(models.Device.device_id == device.device_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Device already exists")

    client_ip = request.client.host
    new_device = models.Device(
        device_id=device.device_id,
        door_id=device.door_id,
        location=client_ip  # Override with client IP
    )

    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device


# ------------------ Get All Devices ------------------ #
@router.get("/list", response_model=list[schemas.DeviceResponse])
def get_all_devices(db: Session = Depends(get_db)):
    return db.query(models.Device).all()

# ------------------ Get Device by ID ------------------ #
@router.get("/{device_id}", response_model=schemas.DeviceResponse)
def get_device(device_id: str, db: Session = Depends(get_db)):
    device = db.query(models.Device).filter(models.Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

# ------------------ Update Device ------------------ #
@router.put("/{device_id}", response_model=schemas.DeviceResponse)
def update_device(device_id: str, updated: schemas.DeviceCreate, db: Session = Depends(get_db)):
    device = db.query(models.Device).filter(models.Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    device.door_id = updated.door_id
    device.location = updated.location
    db.commit()
    db.refresh(device)
    return device
