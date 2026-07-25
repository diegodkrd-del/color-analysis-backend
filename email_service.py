import smtplib
from email.message import EmailMessage
import os

def send_pdf_email(to_email: str, pdf_path: str) -> bool:
    """
    Sends an email with the generated PDF attached.
    Requires SMTP_USER and SMTP_PASS environment variables.
    """
    smtp_server = "smtp.gmail.com"
    smtp_port = 465 # SSL
    
    smtp_user = os.getenv("SMTP_USER", "your-email@gmail.com")
    smtp_pass = os.getenv("SMTP_PASS", "your-app-password")
    
    msg = EmailMessage()
    msg['Subject'] = 'Your Personal Color Analysis Report'
    msg['From'] = smtp_user
    msg['To'] = to_email
    
    msg.set_content(
        "Hello!\n\n"
        "Attached is your beautiful, personalized Color Analysis report.\n"
        "We hope you enjoy exploring your optimal color palette, reading the history "
        "of color analysis, and discovering the mystic vibrations of your true colors.\n\n"
        "Warmly,\n"
        "The Color Analysis Team"
    )
    
    try:
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()
            
        msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename='Color_Analysis_Report.pdf')
        
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        print(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")
        return False
