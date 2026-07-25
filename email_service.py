import smtplib
from email.message import EmailMessage
import os

def send_pdf_email(to_email: str, pdf_path: str, smtp_user: str = None, smtp_pass: str = None) -> bool:
    """
    Sends an email with the generated PDF attached.
    Requires valid SMTP sender email and app password.
    """
    smtp_server = "smtp.gmail.com"
    smtp_port = 465 # SSL
    
    if not smtp_user:
        smtp_user = os.getenv("SMTP_USER", "")
    if not smtp_pass:
        smtp_pass = os.getenv("SMTP_PASS", "")
        
    if not smtp_user or not smtp_pass or "your-email" in smtp_user or "your-app-password" in smtp_pass:
        raise ValueError("SMTP credentials missing. Please enter your Sender Email & Gmail App Password in Studio Settings.")

    msg = EmailMessage()
    msg['Subject'] = 'Your CHROMATYPE Personal Color Analysis Report'
    msg['From'] = f"CHROMATYPE Studio <{smtp_user}>"
    msg['To'] = to_email
    
    msg.set_content(
        "Hello!\n\n"
        "Attached is your personalized CHROMATYPE 15-Page Color Analysis & Virtual Draping Report.\n"
        "We hope you enjoy exploring your optimal color palette, reading the CIE L*a*b* optical science breakdown, "
        "and discovering your true seasonal colors.\n\n"
        "Warmly,\n"
        "The CHROMATYPE Studio Team\n"
        "https://chromatype.me"
    )
    
    try:
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()
            
        filename = os.path.basename(pdf_path)
        msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=filename)
        
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        print(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")
        raise e
