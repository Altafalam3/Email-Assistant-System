import imaplib
import os
import time
import email
from email.header import decode_header
from dotenv import load_dotenv
import streamlit as st
from lib.info import get_email_body
from lib.attachments import extract_attachments
import requests
import agents

# Load environment variables from .env
load_dotenv()

# Streamlit UI setup
st.set_page_config(page_title="Email Assistant Agent", page_icon="📧")

st.title("📧 Email Assistant Agent")
st.write("Monitor your Gmail inbox, classify emails, generate responses effortlessly!")

# User inputs
email_id = st.text_input("Enter your Email ID (Gmail):", value="allu526687@gmail.com")
app_password = st.text_input("Enter your App Password (Gmail):", value="...",type="password")
whatsapp_number = st.text_input("Enter your Whatsapp Number:", value="7021578746")
additional_info = st.text_input("Additional Details which type of emails has more priority to you:", value="I am a SDE so all the major deployments, bugs, glitchs etc are an priority mails for me as after deployment there maybe major issue.")

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

def move_to_folder(imap, mail_id, folder_name):
    """Move email to the specified folder."""
    try:
        imap.copy(mail_id, folder_name)
        imap.store(mail_id, "+FLAGS", "\\Deleted")
        imap.expunge()
    except Exception as e:
        st.error(f"Error moving email to folder {folder_name}: {e}")

def add_label(imap, mail_id, label):
    """Add a label to the email."""
    try:
        imap.store(mail_id, "+X-GM-LABELS", label)
    except Exception as e:
        st.error(f"Error adding label {label}: {e}")

def save_to_draft(imap, email_id, subject, body):
    """Save a response to the draft folder."""
    try:
        draft_email = f"Subject: {subject}\nFrom: {email_id}\nTo: {email_id}\n\n{body}"
        imap.append("[Gmail]/Drafts", "", imaplib.Time2Internaldate(time.time()), draft_email.encode("utf-8"))
    except Exception as e:
        st.error(f"Error saving draft: {e}")

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
                    body += "\n\n".join(attachments)
                    
                    # Call agents logic
                    email_analysis = agents.process_email(
                        sender=sender,
                        subject=subject,
                        body=body,
                        user_email=email_id,
                        additional_info=additional_info,
                    )
                    
                    content_analysis = email_analysis.get("content_analysis", {})
                    priority_decision = email_analysis.get("priority_decision", {})
                    response_action = email_analysis.get("response_action", {})
                    print(content_analysis)
                    print(response_action)
                    # Display email details in Streamlit expander
                    with st.expander(f"📩 {subject}"):
                        st.write(f"**From:** {sender}")
                        st.write(f"**Subject:** {subject}")
                        st.write(f"**Body:**\n\n{body}")
                        st.write(f"**Priority:** {priority_decision.get('priority', 'Unknown')}")
                        st.write(f"**Response:** {response_action.get('response', 'No response generated')}")

                    # Handle email actions based on priority
                    if priority_decision.get("spam"):
                        st.write("Email marked as spam and moved to Spam folder.")
                        move_to_folder(imap, mail_id, "[Gmail]/Spam")
                    elif priority_decision.get("priority"):
                        
                        # Add label, save to drafts, and notify via WhatsApp
                        add_label(imap, mail_id, "High Priority")
                        save_to_draft(
                            imap,
                            email_id=email_id,
                            subject=f"RE: {subject}",
                            body=response_action.get("response", "No response available"),
                        )
                        st.write("High-priority email labeled and response saved to drafts.")
                        requests.post(
                            "http://localhost:8801/api/notification",
                            json={
                                "number": whatsapp_number,
                                "message": f"High Priority Email from {sender}: {subject}",
                            }
                        )

                    elif not priority_decision.get("priority"):
                        # Add label for low-priority emails
                        add_label(imap, mail_id, "Low Priority")
                        st.write("Low-priority email labeled.")

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
