from fastapi import FastAPI
import uvicorn

from app.routes import employee, auth, qr, attendance, device  # Make sure attendance route is imported
from app.models import Base
from app.database import engine

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(employee.router, prefix="/employee", tags=["Employee"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(qr.router, prefix="/qr", tags=["QR"])
app.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])  # NEW
app.include_router(device.router, prefix="/devices", tags=["Devices"])

# Run the app
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
