import smtplib
from email.mime.text import MIMEText
from email.header import Header

class emailbox():
    def __init__(self, smtp_server, smtp_port, sender, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender = sender
        self.password = password
    def send_email(self, subject, body, receiver):
        message = MIMEText(body, 'plain', 'utf-8')
        message['From'] = Header("Science Agent", 'utf-8')
        message['To'] = Header("User", 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
            smtp.starttls()
            smtp.login(self.sender, self.password)
            smtp.sendmail(self.sender, receiver, message.as_string())
            smtp.quit()
            return True
        except Exception as e:
            print(f"Email fail code: {e}")
            return False