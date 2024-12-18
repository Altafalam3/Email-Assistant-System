import imaplib
import os
import time
import email
from email.header import decode_header
from dotenv import load_dotenv
import streamlit as st
from lib.info import get_email_body
from lib.attachments import extract_attachments

import llm

# Load environment variables from .env
load_dotenv()

# Streamlit UI setup
st.set_page_config(page_title="Email Assistant Agent", page_icon="📧")

st.title("📧 Email Assistant Agent")
st.write("Monitor your Gmail inbox, classify emails, generate responses effortlessly!")

# User inputs
email_id = st.text_input("Enter your Email ID (Gmail):", value="allu526687@gmail.com")
app_password = st.text_input("Enter your App Password (Gmail):", value="bada sybq jymf khuv", type="password")
monitor = st.button("Start Monitoring")

def safe_decode(value, encoding=None):
    """Safely decode email headers or body content."""
    try:
        if isinstance(value, bytes):
            if encoding is None:  # Skip decoding if encoding is None
                return value
            return value.decode(encoding, errors="ignore")
        return str(value)
    except Exception:
        return "Unable to decode content"

if monitor and email_id and app_password:
    try:
        # Connect to Gmail IMAP server
        st.info("Connecting to Gmail IMAP server...")
        imap_server = os.getenv("GMAIL_IMAP_SERVER", "imap.gmail.com")
        imap_port = os.getenv("GMAIL_IMAP_PORT", 993)

        imap = imaplib.IMAP4_SSL(imap_server, imap_port)
        imap.login(email_id, app_password)

        st.success("Connected successfully!")
        st.info("Monitoring your inbox for unread emails...")

        while True:
            imap.select("INBOX")
            status, messages = imap.search(None, "UNSEEN")

            if status == "OK" and messages[0]:
                for mail_id in messages[0].split():
                    # Fetch email
                    _, msg_data = imap.fetch(mail_id, "(RFC822)")
                    raw_email = msg_data[0][1]
                    email_message = email.message_from_bytes(raw_email)

                    # Extract email details with fallback decoding
                    subject_header = decode_header(email_message.get("Subject", "No Subject"))
                    subject = " ".join(
                        safe_decode(part[0], part[1]) for part in subject_header
                    )

                    sender = safe_decode(email_message.get("From", "Unknown Sender"))
                    body = get_email_body(email_message)
                    attachments = extract_attachments(email_message)

                    # Display email details
                    with st.expander(f"📩 {subject}"):
                        st.write(f"**From:** {sender}")
                        st.write(f"**Subject:** {subject}")
                        st.write(f"**Body:**\n\n{body}")

                        if attachments:
                            st.write("**Attachments:**")
                            for attachment in attachments:
                                st.write(f"- {attachment}")

                    # Mark email as read
                    imap.store(mail_id, "+FLAGS", "\\Seen")

            else:
                st.info("No new unread emails.")

            # Poll inbox every 10 seconds
            time.sleep(10)

    except Exception as e:
        st.error(f"An error occurred: {e}")

    finally:
        imap.logout()
