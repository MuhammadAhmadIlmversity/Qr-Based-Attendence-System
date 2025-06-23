from fastapi import APIRouter, HTTPException, Request
from app.qr.generator import generate_token, generate_qr_image
from app.qr.validator import validate_token
from app.crud import is_employee_authorized_for_door
from app.database import SessionLocal
from app import crud, models
from datetime import datetime, time, timedelta

router = APIRouter()



@router.get("/current")
def get_qr_image(emp_id: str):
    token = generate_token(emp_id)
    image_b64 = generate_qr_image(token)
    return {"qr_code": image_b64, "token": token}

@router.post("/scan")
def scan_qr(token: str, device_id: str, door_id: str, request: Request):
    emp_id = validate_token(token)
    if not emp_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    client_ip = request.client.host
    db = SessionLocal()
    try:
        # 1. Verify Device
        device = db.query(models.Device).filter(models.Device.device_id == device_id).first()
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        if device.location != client_ip:
            raise HTTPException(
                status_code=403,
                detail=f"IP address mismatch. Unauthorized device. Expected: {device.location}, Got: {client_ip}"
            )

        # 2. Check Access Rights
        authorized = is_employee_authorized_for_door(db, emp_id, door_id)
        if not authorized:
            raise HTTPException(status_code=403, detail="Unauthorized door access")

        # 3. Enforce 10-minute lockout
        ten_minutes_ago = datetime.utcnow() - timedelta(minutes=10)
        recent_attempt = db.query(models.Attendance).filter(
            models.Attendance.emp_id == emp_id,
            models.Attendance.check_in_time != None,
            models.Attendance.check_in_time >= ten_minutes_ago
        ).first()
        if recent_attempt:
            raise HTTPException(status_code=403, detail="Too many attempts. Please wait 10 minutes.")

        # 4. Decide Automatically: Check-in or Check-out
        now = datetime.utcnow().time()
        if now < time(19, 0):  # before 7 PM → Check-in
            success, message = crud.record_check_in(db, emp_id, device_id)
        else:  # after 7 PM → Check-out
            success, message = crud.record_check_out(db, emp_id, device_id)

        if not success:
            raise HTTPException(status_code=403, detail=message)

        return {"success": True, "message": message}
    finally:
        db.close()
