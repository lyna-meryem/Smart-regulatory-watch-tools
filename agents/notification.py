"""
Notification Agent (Agent 4)
----------------------------
This agent is responsible for generating alerts when the Keyword Analysis Agent
detects relevant content in regulatory documents.

It supports:
 - Streamlit notifications (always active)
 - Optional email notifications using SMTP, or simulated emails if SMTP is not configured
"""

import smtplib
from email.mime.text import MIMEText
import streamlit as st


class NotificationAgent:

    def __init__(
        self,
        smtp_server=None,
        smtp_user=None,
        smtp_password=None,
        from_email="no-reply@datathon.com",
    ):
        self.smtp_server = smtp_server
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.from_email = from_email

    # --------------------------------------------------------------------------
    # STREAMLIT NOTIFICATION
    # --------------------------------------------------------------------------
    def streamlit_notify(self, analysis_result: dict):
        """
        Displays a Streamlit notification.

        Parameters
        ----------
        analysis_result : dict containing:
            - filename
            - bank
            - keywords (list)
            - summary
            - timestamp

        Returns dict with status metadata
        """
        filename = analysis_result.get("filename")
        bank = analysis_result.get("bank")
        keywords = analysis_result.get("keywords", [])
        summary = analysis_result.get("summary")
        timestamp = analysis_result.get("timestamp")

        st.success(f"🔔 Nouveau document analysé ({bank}) : {filename}")
        st.info(f"✨ Mots clés détectés : {', '.join(keywords) if keywords else 'Aucun'}")
        st.write(f"🕒 Analyse effectuée à : {timestamp}")
        st.write("📝 Résumé du document :")
        st.write(summary)

        return {
            "status": "ok",
            "filename": filename,
            "keywords": keywords,
            "timestamp": timestamp,
        }

    # --------------------------------------------------------------------------
    # EMAIL NOTIFICATION
    # --------------------------------------------------------------------------
    def send_email(self, to_email: str, subject: str, body: str):
        """
        Sends an email if SMTP is configured, otherwise simulates it.

        Returns dict with email sending result.
        """

        if not to_email:
            return {"status": "no_email", "message": "No destination email provided."}

        # If no SMTP configured → simulate email sending
        if not self.smtp_server:
            return {
                "status": "simulated",
                "to": to_email,
                "subject": subject,
                "body": body,
            }

        # Real SMTP sending
        try:
            msg = MIMEText(body, "plain", "utf-8")
            msg["Subject"] = subject
            msg["From"] = self.from_email
            msg["To"] = to_email

            with smtplib.SMTP(self.smtp_server, 587) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            return {"status": "sent", "to": to_email}

        except Exception as e:
            return {"status": "error", "detail": str(e)}

    # --------------------------------------------------------------------------
    # FULL WORKFLOW: notify() = Streamlit + Email
    # --------------------------------------------------------------------------
    def notify(self, analysis_result: dict, email: str = None):
        """
        Main method used by the scheduler.
        It triggers both Streamlit + Email notifications.

        Returns dict:
            {
              "streamlit": {...},
              "email": {...}
            }
        """

        if not isinstance(analysis_result, dict):
            raise Exception("Invalid analysis_result format. Must be a dict.")

        streamlit_result = self.streamlit_notify(analysis_result)

        subject = f"[Regulatory Watch] Keywords detected in {analysis_result.get('filename')}"
        body = f"""
Document: {analysis_result.get('filename')}
Bank: {analysis_result.get('bank')}
Keywords: {', '.join(analysis_result.get('keywords', []))}
Timestamp: {analysis_result.get('timestamp')}

Summary:
{analysis_result.get('summary')}
"""

        email_result = self.send_email(email, subject, body)

        return {
            "streamlit": streamlit_result,
            "email": email_result,
        }
 