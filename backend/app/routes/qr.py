from fastapi import APIRouter, HTTPException, Request
from app.qr.generator import generate_token, generate_qr_image
from app.qr.validator import validate_token
from app.crud import record_check_in, record_check_out
from app.database import SessionLocal
from app import crud, models


router = APIRouter()

@router.get("/current")
def get_qr_image(emp_id: str):
    token = generate_token(emp_id)
    image_b64 = generate_qr_image(token)
    return {"qr_code": image_b64, "token": token}

@router.post("/scan")
def scan_qr(token: str, mode: str, device_id: str, request: Request):
    emp_id = validate_token(token)
    if not emp_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    client_ip = request.client.host

    db = SessionLocal()
    try:
        # Fetch device
        device = db.query(models.Device).filter(models.Device.device_id == device_id).first()
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")

        if device.location != client_ip:
            raise HTTPException(status_code=403, detail="IP address mismatch. Unauthorized device.")

        # Proceed with attendance
        if mode == "in":
            success, message = crud.record_check_in(db, emp_id, device_id)
        elif mode == "out":
            success, message = crud.record_check_out(db, emp_id, device_id)
        else:
            raise HTTPException(status_code=400, detail="Invalid mode")

        if not success:
            raise HTTPException(status_code=403, detail=message)

        return {"success": True, "message": message}
    finally:
        db.close()

