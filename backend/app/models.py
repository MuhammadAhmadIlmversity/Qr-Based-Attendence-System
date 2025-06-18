from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Employee(Base):
    __tablename__ = "employees"
    emp_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    pin = Column(String)

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(String, primary_key=True, index=True)
    emp_id = Column(String, ForeignKey("employees.emp_id"))
    check_in_time = Column(DateTime, nullable=True)
    check_out_time = Column(DateTime, nullable=True)
    device_id = Column(Integer, ForeignKey("devices.device_id"))

    employee = relationship("Employee", backref="attendance")

class Device(Base):
    __tablename__ = "devices"

    device_id = Column(String, primary_key=True, index=True)
    location = Column(String, nullable=True)  # Stores IP address or geolocation
    door_id = Column(String, nullable=False)