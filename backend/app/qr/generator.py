import time
import hmac
import hashlib
import base64
import qrcode
from io import BytesIO
import os

SECRET_KEY = os.getenv("QR_SECRET_KEY", "defaultsecret")

def generate_token(employee_id: str) -> str:
    timestamp = int(time.time() // 60)  # 30-second intervals
    message = f"{employee_id}:{timestamp}"
    signature = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()
    return f"{employee_id}:{timestamp}:{signature}"

def generate_qr_image(token: str) -> str:
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(token)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")
