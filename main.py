#!/usr/bin/env python
# coding: utf-8

from scripts.fetch_quote_from_api import fetch_quote
from scripts.fetch_users import get_active_users
from scripts.connect_to_db import get_connection
from scripts.send_email import send_email
from dotenv import load_dotenv
from scripts.logger import configure_logging
from datetime import datetime
import os
import pandas as pd  

load_dotenv()
LOG_FILE = os.getenv("LOG_FILE_QUOTE")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

logger = configure_logging()

def main():
    """Main workflow to fetch quote, get users, send emails, and send summary to admin."""

    logger.info("Fetching quote...")
    quote, author = fetch_quote()
    
    if not quote:
        logger.error("Aborting: No quote available in Zenqoute API today.")
        return

    logger.info(f"Quote fetched: “{quote}” — {author}")
    logger.info("Preparing to send emails to users...")
    
    USERS = get_active_users()
    logger.info(f"Total active users to email: {len(USERS)}")

    total_users = len(USERS)
    success_count = 0
    fail_count = 0
    retry_events = []
    
    conn = get_connection()

    for user_id in list(USERS["user_id"]):
        logger.info(f"Connected to database to update last_emailed for user_id: {user_id}")

        last_emailed = USERS.loc[USERS["user_id"] == user_id, "last_emailed"].values[0]
        email_frequency = USERS.loc[USERS["user_id"] == user_id, "email_frequency"].values[0]
        name = USERS.loc[USERS["user_id"] == user_id, "name"].values[0]
        user_email = USERS.loc[USERS["user_id"] == user_id, "email"].values[0]

        personalized_body = (
            f"Hello {name},\n\n"
            f"Today's quote:\n\n“{quote}” by author: {author}\n\n"
            "Stay inspired,\nFrom Your Daily Quote Service MindFuel"
        )
        subject = f"Your Daily Quote from MindFuel"

        success = send_email(user_email, subject, personalized_body, attachments=None, last_emailed=last_emailed, email_frequency=email_frequency)
        
        if success:
            success_count += 1
            user_id_to_update = user_id

            conn.execute("""
                UPDATE users
                SET last_emailed = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, [user_id_to_update])
        else:
            fail_count += 1
            retry_events.append(user_email)
    conn.close()
    logger.info("Database connection closed.")

    # Prepare daily summary for admin
    summary = (
        f"Daily Quote Summary - {datetime.now().strftime('%Y-%m-%d')}\n\n"
        f"Total users: {total_users}\n"
        f"Emails sent successfully: {success_count}\n"
        f"Failed deliveries: {fail_count}\n"
        f"Retried users: {', '.join(retry_events) if retry_events else 'None'}\n"
        f"\nQuote: “{quote}” — {author}"
    )
    
    logger.info("Preparing to send daily summary to admin...")
    # Send summary email to admin with log attachment
    send_email(
        ADMIN_EMAIL,
        "Daily Quote Service Summary (with Logs)",
        summary,
        attachments=[LOG_FILE]
    )
    logger.info(f"Daily summary sent to admin {ADMIN_EMAIL}")
    logger.info("Email delivery process completed. Check log for details.")
    
if __name__ == "__main__":
    main()