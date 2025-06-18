import time
import hmac
import hashlib
import os

SECRET_KEY = os.getenv("QR_SECRET_KEY", "defaultsecret")

def validate_token(token: str) -> str | None:
    try:
        emp_id, timestamp, received_sig = token.split(":")
        timestamp = int(timestamp)

        # Token must be within last 30s
        current = int(time.time() // 60)
        if abs(current - timestamp) > 1:
            return None

        expected_msg = f"{emp_id}:{timestamp}"
        expected_sig = hmac.new(SECRET_KEY.encode(), expected_msg.encode(), hashlib.sha256).hexdigest()
        
        if hmac.compare_digest(received_sig, expected_sig):
            return emp_id
        return None
    except:
        return None
