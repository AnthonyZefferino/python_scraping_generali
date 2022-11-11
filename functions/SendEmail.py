import smtplib, pprint
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from pathlib import Path
from datetime import datetime


def SendEmail(Subject, MessageBody):
    dotenv_path = Path('C:\scraping\scrapingGenerali.env.development')
    load_dotenv(dotenv_path=dotenv_path)

    if os.getenv('ENVIROMENT_PLACEHOLDER') == 'T':
        return False

    html = """\
    <html>
      <body>
         """ + MessageBody + """
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects

    part2 = MIMEText(html, "html")
    now = datetime.now()
    message = MIMEMultipart("alternative")
    message["Subject"] = os.getenv('ENVIROMENT') + Subject + " " + datetime.timestamp(now)
    message["From"] = os.getenv('SMTP_USERNAME')
    message["To"] = [os.getenv('EMAIL_ERROR')]

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first

    message.attach(part2)
    text_subtype = 'plain'

    try:
        conn = SMTP(os.getenv('SMTP_HOST'), os.getenv('PORT'))
        # conn.set_debuglevel(1)
        conn.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD'))
        try:

            conn.sendmail(os.getenv('SMTP_USERNAME'), message["To"], message.as_string())

        finally:
            conn.quit()

    except smtplib.SMTPRecipientsRefused as e:
        a = e
        pprint(a)
