import os
import smtplib
import numpy as np
import pandas as pd 
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv 
from scripts.logger import configure_logging

# Load environment variables from .env file
load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD") 
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT_SSL = os.getenv("SMTP_PORT_SSL")

logger = configure_logging()

def send_email(to_email, subject, body, attachments=None, last_emailed = None, email_frequency=None, retries=3, delay=5):
    """
    Sends an email (with optional attachments) to User's email or an admin email address.
    Includes retry logic and works with Gmail App Passwords.
    """
    for attempt in range(1, retries + 1):
        try:
            # Build Email
            msg = MIMEMultipart()
            msg["From"] = SENDER_EMAIL
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            # Attach Files (if provided)
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            part = MIMEBase("application", "octet-stream")
                            part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            "Content-Disposition",
                            f"attachment; filename={os.path.basename(file_path)}",
                        )
                        msg.attach(part)
                    else:
                        logger.warning(f"Attachment not found: {file_path}")

            # Send Email via Gmail (SSL connection preferred)
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT_SSL) as server:
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                      
                now = datetime.now()

                if email_frequency is None and last_emailed is None:
                    server.send_message(msg)
                    logger.info(f"Email send to Admin email: {to_email}")
                else:
                    # Calculate difference in hours
                    if isinstance(last_emailed, np.datetime64):
                        last_emailed = pd.to_datetime(last_emailed).to_pydatetime()

                    elif isinstance(last_emailed, str):
                        last_emailed = datetime.fromisoformat(last_emailed)

                    hours_since_last = (now - last_emailed).total_seconds() / 3600
                    print(f"Hours since last emailed: {hours_since_last}")

                    if email_frequency == 'daily' and hours_since_last >= 24:
                        server.send_message(msg)
                    elif email_frequency == 'weekly' and hours_since_last >= 168:
                        server.send_message(msg)
                    else:
                        logger.info(f"Email to {to_email} not sent due to frequency settings.")
                        return False  # Considered success as per frequency settings
            logger.info(f"Success: Email sent to {to_email}")
            return True

        except smtplib.SMTPAuthenticationError:
            logger.error("Authentication failed. Check Gmail App Password or account settings.")
            break  # no need to retry if credentials are wrong

        except smtplib.SMTPServerDisconnected:
            logger.warning(f"Attempt {attempt}: Connection unexpectedly closed. Retrying...")
            time.sleep(delay)

        except Exception as e:
            logger.warning(f"Attempt {attempt} failed for {to_email}: {e}")
            time.sleep(delay)

    logger.error(f"Failed to send email to {to_email} after {retries} retries.")
    print(f"Failed to send email to {to_email} after {retries} retries.")
    return False

if __name__ == "__main__":
    send_email()