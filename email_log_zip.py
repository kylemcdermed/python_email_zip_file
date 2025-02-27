import smtplib
import logging
import zipfile
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create the .env file 
with open('.env', 'w') as f:
    f.write(""" 
EMAIL_USER="kylemcdermed1@gmail.com"
EMAIL_PASS=""
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=587
""")

# Get credentials from environment variables
smtp_server = os.getenv("SMTP_SERVER")  
smtp_port = int(os.getenv("SMTP_PORT", 587))  
from_address = os.getenv("EMAIL_USER")  
password = os.getenv("EMAIL_PASS")  
to_address = "kylemcdermed1@gmail.com" 

log_file = 'email_test.log'
zip_file = 'zip_file.zip'

# Set up logging 
logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file, mode='a')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Log each step 
logger.info("Script started.")

try:
    logger.info('Initializing SMTP object')
    smtp_object = smtplib.SMTP(smtp_server, smtp_port)
    
    logger.info('Performing EHLO handshake')
    smtp_object.ehlo()
    
    logger.info('Starting TLS encryption')
    smtp_object.starttls()
    
    logger.info('Logging into SMTP server')
    smtp_object.login(from_address, password)

    logger.info('Preparing email with all contents')
    # Prepare email
    msg = EmailMessage()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Automated Email Test"
    msg.set_content("Hi Kyle,\nThis is my first time sending an email using python and attaching a logging zip file.\nBest,\nKyle")

    # Attach log file
    logger.info('Zipping log file before attachment')

    logger.warning('Ensuring all logs are written before zipping')
    # Ensure all logs are written before zipping
    for handler in logger.handlers:
        handler.flush()

    logger.info('Writing zip file...')
    with zipfile.ZipFile(zip_file, mode='w', compression=zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(log_file)

    logger.info('Reading zip file as binary to attach to message')
    with open(zip_file, 'rb') as f:
        zip_data = f.read()
        msg.add_attachment(zip_data, maintype='application', subtype='zip', filename=os.path.basename(zip_file))
    
    logger.warning('Sending email with attachment')
    smtp_object.send_message(msg)

    logger.info('Email sent successfully!')

except smtplib.SMTPException as e:
    logger.error(f'SMTP error occurred: {e}')
except Exception as e:
    logger.error(f'Error occurred: {e}')
finally:
    if 'smtp_object' in locals() and smtp_object.sock:
        smtp_object.quit()
        logger.info("SMTP session closed.")
    else:
        logger.error("SMTP session was never established.")
