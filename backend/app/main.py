from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.routes import employee, auth, qr, attendance, device, access
from app.models import Base
from app.database import engine

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

origins = [
    "http://localhost:3000",  # React frontend
    # Add production URL here later if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # Allows requests from frontend
    allow_credentials=True,
    allow_methods=["*"],                # Allows all HTTP methods
    allow_headers=["*"],                # Allows all headers
)

# Include routers
app.include_router(employee.router, prefix="/employee", tags=["Employee"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(qr.router, prefix="/qr", tags=["QR"])
app.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])  # NEW
app.include_router(device.router, prefix="/devices", tags=["Devices"])
app.include_router(access.router, prefix="/access", tags=["Access"])  # ← add this line

# Run the app
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
