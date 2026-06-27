import imaplib
import email
from datetime import datetime, timedelta
class GmailLoader:
    def __init__(self, email_address, app_password):
        self.email = email_address
        self.password = app_password

    def fetch_emails(self, days=7, max_emails=15):
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(self.email, self.password)
        mail.select("inbox")

        date_since = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
        status, messages = mail.search(None, f'(SINCE "{date_since}")')
        email_ids = messages[0].split()[-max_emails:]

        documents = []
        for e_id in email_ids:
            status, msg_data = mail.fetch(e_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            body = self._get_email_body(msg)

            subject = msg.get("Subject", "No Subject")
            sender = msg.get("From", "Unknown Sender")
            date_str = msg.get("Date", "Unknown Date")

            content = f"Date: {date_str}\nFrom: {sender}\nSubject: {subject}\n\n{body}"
            documents.append({
                "page_content": content,
                "metadata": {
                    "source": "gmail",
                    "sender": sender,
                    "subject": subject,
                    "date": date_str,
                }
            })

        mail.close()
        mail.logout()
        return documents

    def _get_email_body(self, msg):
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
                    except:
                        continue
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        return body[:1500] if body else "[No body content]"
