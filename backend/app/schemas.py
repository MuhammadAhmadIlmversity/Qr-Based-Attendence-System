from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ------------------ Employee ------------------ #

class EmployeeBase(BaseModel):
    emp_id: str
    name: str

class EmployeeCreate(EmployeeBase):
    pin: str

class EmployeeResponse(EmployeeBase):
    class Config:
        orm_mode = True

# ------------------ Authentication ------------------ #

class QRRequest(BaseModel):
    qr_token: str

class PINRequest(BaseModel):
    emp_id: str
    pin: str

class AuthResponse(BaseModel):
    success: bool
    message: str

class QRToken(BaseModel):
    token: str

# ------------------ Device ------------------ #

class DeviceBase(BaseModel):
    device_id: str
    door_id: str
    location: Optional[str] = None # IP address or GPS coordinate

class DeviceCreate(DeviceBase):
    pass

class DeviceResponse(DeviceBase):
    class Config:
        orm_mode = True

# ------------------ Attendance ------------------ #

class AttendanceOut(BaseModel):
    emp_id: str
    check_in_time: Optional[datetime]
    check_out_time: Optional[datetime]
    device_id: Optional[str]  # NEW: Show which device was used

    class Config:
        orm_mode = True

class AttendanceCreate(BaseModel):
    emp_id: str
    device_id: str

# ------------------ AccessMapping ------------------ #

class AccessMappingBase(BaseModel):
    emp_id: str
    door_id: str

class AccessMappingCreate(AccessMappingBase):
    pass

class AccessMappingResponse(AccessMappingBase):
    id: int

    class Config:
        orm_mode = True