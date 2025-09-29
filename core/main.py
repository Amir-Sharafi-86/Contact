from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from email.message import EmailMessage
import aiosmtplib, os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "benxfoxy@gmail.com"
SMTP_PASS = "rjes bdxo dlrq tpel"  # replace with your Gmail App Password
TO_EMAIL   = "benxfoxy@gmail.com"
FROM_EMAIL = SMTP_USER

class ContactSchema(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    phone_number: str
    description: str

def build_contact_email(p: ContactSchema) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = f"New contact request from {p.name} {p.last_name}"
    msg.set_content(f"""You have a new contact request:

Name: {p.name} {p.last_name}
Email: {p.email}
Phone: {p.phone_number}

Message:
{p.description}
""")
    return msg

@app.post("/contact")
async def contact(payload: ContactSchema):
    msg = build_contact_email(payload)

    # Send INLINE (reliable on serverless)
    try:
        await aiosmtplib.send(
            msg,
            hostname=SMTP_HOST, port=SMTP_PORT, start_tls=True,
            username=SMTP_USER, password=SMTP_PASS,
        )
    except Exception as e:
        # log e in real code
        raise HTTPException(status_code=502, detail=f"Email send failed: {e}")

    return {"message": "Your message has been sent successfully."}

@app.get("/health")
def health():
    return {"ok": True}
