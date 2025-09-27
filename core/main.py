from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, Field, EmailStr
from email.message import EmailMessage
import aiosmtplib

app = FastAPI()

# --- Settings (use env vars in production) ---
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "benxfoxy@gmail.com"
SMTP_PASS = "rjes bdxo dlrq tpel"  # replace with your Gmail App Password
TO_EMAIL   = "benxfoxy@gmail.com"
FROM_EMAIL = SMTP_USER

# --- Schema ---
class ContactSchema(BaseModel):
    name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr
    phone_number: str = Field(...)
    description: str = Field(...)


# --- Build and send email ---
def build_contact_email(payload: ContactSchema) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = f"New contact request from {payload.name} {payload.last_name}"

    body = f"""
    You have a new contact request:

    Name: {payload.name} {payload.last_name}
    Email: {payload.email}
    Phone: {payload.phone_number}

    Message:
    {payload.description}
    """
    msg.set_content(body)
    return msg


async def send_email_message(msg: EmailMessage):
    await aiosmtplib.send(
        msg,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        start_tls=True,
        username=SMTP_USER,
        password=SMTP_PASS,
    )


# --- Route ---
@app.post("/")
async def contact(payload: ContactSchema, bg: BackgroundTasks):
    msg = build_contact_email(payload)
    # send in background so API is fast
    bg.add_task(send_email_message, msg)
    return {"message": "Your message has been sent successfully."}
