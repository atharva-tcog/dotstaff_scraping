# mail_reader.py
import imaplib
import email
import re
from datetime import datetime
from email.header import decode_header
from email.utils import parsedate_tz, mktime_tz
from bs4 import BeautifulSoup
from logger import get_logger

logger = get_logger(__name__)

class MailReader:

    def __init__(self, username, password):  #global_time
        self.username = username
        self.password = password
        # self.global_time = global_time

    def fetch_unseen_dotstaff_mails(self):
        FROM_FILTER = "requirements@tcognition.com"
        mail_data = []
        update_mail_data = []

        # logger.info(f"Reading mails for date: {self.global_time}")

        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(self.username, self.password)
        imap.select("INBOX")

        status, unseen_msg = imap.search(None, "UNSEEN")
        mail_ids = unseen_msg[0].split()

        if not mail_ids:
            logger.info("No unseen emails found")
            return mail_data, update_mail_data

        for msg_id in mail_ids:
            _, msg_data = imap.fetch(msg_id, "(RFC822)")

            for response in msg_data:
                if not isinstance(response, tuple):
                    continue

                msg = email.message_from_bytes(response[1])

                from_addr, enc = decode_header(msg.get("From"))[0]
                if isinstance(from_addr, bytes):
                    from_addr = from_addr.decode(enc or "utf-8", errors="ignore")

                if FROM_FILTER.lower() not in from_addr.lower():
                    continue

                subject, enc = decode_header(msg.get("Subject"))[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(enc or "utf-8", errors="ignore").strip()

                post_id_match = re.search(r"\b\d{6}\b", subject)
                post_id = post_id_match.group() if post_id_match else None

                email_date_raw = msg["Date"]
                dt_tuple = parsedate_tz(email_date_raw)
                post_date = datetime.fromtimestamp(mktime_tz(dt_tuple))

                body = self._extract_body(msg)

                mail_data.append([
                    post_id,
                    post_date,
                    subject,
                    body,
                    msg["Message-ID"]
                ])

        imap.close()
        imap.logout()

        logger.info(f"Fetched {len(mail_data)} DOTSTAFF mails")
        return mail_data, update_mail_data

    def _extract_body(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() in ["text/plain", "text/html"]:
                    try:
                        content = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                        return BeautifulSoup(content, "html.parser").get_text().strip()
                    except Exception:
                        pass
        else:
            content = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
            return BeautifulSoup(content, "html.parser").get_text().strip()
        return ""