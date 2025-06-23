from sqlalchemy.orm import Session
from datetime import datetime, time
from app import models, schemas
import uuid

# ------------------ Employee Logic ------------------ #

def get_employee_by_id(db: Session, emp_id: str):
    return db.query(models.Employee).filter(models.Employee.emp_id == emp_id).first()

def get_all_employees(db: Session):
    return db.query(models.Employee).all()

def create_employee(db: Session, emp: schemas.EmployeeCreate):
    new_emp = models.Employee(
        emp_id=emp.emp_id,
        name=emp.name,
        pin=emp.pin
    )
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp

def verify_pin(db: Session, emp_id: str, pin: str):
    emp = get_employee_by_id(db, emp_id)
    return emp and emp.pin == pin

def check_out_employee(db: Session, emp_id: str):
    emp = db.query(models.Employee).filter(models.Employee.emp_id == emp_id).first()
    if emp:
        emp.last_checkout = datetime.utcnow()
        db.commit()

# ------------------ Attendance Logic ------------------ #

def get_today_attendance(db: Session, emp_id: str):
    today = datetime.utcnow().date()
    return db.query(models.Attendance).filter(
        models.Attendance.emp_id == emp_id,
        models.Attendance.check_in_time >= datetime.combine(today, time(0, 0))
    ).first()

def record_check_in(db: Session, emp_id: str, device_id: str):
    now = datetime.utcnow()
    if now.time() >= time(19, 0):
        return False, "Check-in not allowed after 7:00 PM"

    existing = get_today_attendance(db, emp_id)
    if existing:
        return False, "Already checked in today"

    record = models.Attendance(
        id=str(uuid.uuid4()),
        emp_id=emp_id,
        check_in_time=now,
        device_id=device_id  # ← store which device was used
    )
    db.add(record)
    db.commit()
    return True, "Check-in successful"

def record_check_out(db: Session, emp_id: str, device_id: str):
    now = datetime.utcnow()
    if now.time() < time(19, 0):
        return False, "Check-out not allowed before 7:00 PM"

    record = get_today_attendance(db, emp_id)
    if not record:
        return False, "Cannot check out without checking in"
    if record.check_out_time:
        return False, "Already checked out today"

    record.check_out_time = now
    record.device_id = device_id  # Update or override device used for checkout
    db.commit()
    return True, "Check-out successful"


def get_attendance_by_employee(db: Session, emp_id: str):
    return db.query(models.Attendance).filter(
        models.Attendance.emp_id == emp_id
    ).order_by(models.Attendance.check_in_time.desc()).all()

def get_all_attendance(db: Session):
    return db.query(models.Attendance).order_by(
        models.Attendance.check_in_time.desc()
    ).all()

# ------------------ AccessMapping ------------------ #

def create_access_mapping(db: Session, mapping: schemas.AccessMappingCreate):
    new_mapping = models.AccessMapping(
        emp_id=mapping.emp_id,
        door_id=mapping.door_id
    )
    db.add(new_mapping)
    db.commit()
    db.refresh(new_mapping)
    return new_mapping

def get_employee_access_doors(db: Session, emp_id: str):
    return db.query(models.AccessMapping).filter(models.AccessMapping.emp_id == emp_id).all()

def is_employee_authorized_for_door(db: Session, emp_id: str, door_id: str):
    return db.query(models.AccessMapping).filter(
        models.AccessMapping.emp_id == emp_id,
        models.AccessMapping.door_id == door_id
    ).first() is not None

from datetime import timedelta

def is_locked_out(db: Session, emp_id: str) -> bool:
    ten_min_ago = datetime.utcnow() - timedelta(minutes=10)
    recent_attempt = db.query(models.Attendance).filter(
        models.Attendance.emp_id == emp_id,
        models.Attendance.check_in_time != None,
        models.Attendance.check_in_time >= ten_min_ago
    ).first()
    return bool(recent_attempt)
