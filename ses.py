import boto3
from botocore.exceptions import NoCredentialsError
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import shutil
import zipfile

 

# Set your AWS credentials
aws_access_key = 'AKIA6LBJHUQAJT5JTVYC'
aws_secret_key = 'JHvBAaj+Z34udBH2zi44eTvyKIrkBNqml5fNW4kb'
region = 'us-east-1'  # Change to your desired AWS region 

 

# Set email parameters
sender_email = 'rijomathew555@gmail.com'
recipient_email = 'mathewrijo23@gmail.com'
subject = 'Test email with attachment'
body_text = 'This is a test email with an attachment sent from boto3.'
body_html = '<html><body><h1>This is a test email with an attachment sent from boto3.</h1></body></html>'

 # Directory to be attached
directory_to_attach = '/home/runner/work/workflows/workflows/2023-08-11-ZAP-Report-dev-bo.nephroplus.com'

# Path to the file you want to attach
attachment_file_path = '/home/runner/work/workflows/workflows/zap_report.zip'

# Create a zip archive of the directory
shutil.make_archive(attachment_file_path.rstrip('.zip'), 'zip', directory_to_attach)
 

# Connect to Amazon SES
ses = boto3.client('ses', region_name=region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

 

# Read the content of the attachment file
with open(attachment_file_path, 'rb') as attachment_file:
    attachment_content = attachment_file.read()

 

# Create a MIME Multipart message
msg = MIMEMultipart('mixed')
msg['Subject'] = subject
msg['From'] = sender_email
msg['To'] = recipient_email

 

# Attach the text part
msg.attach(MIMEText(body_text, 'plain'))
msg.attach(MIMEText(body_html, 'html'))

 

# Attach the file
attachment_mime = MIMEApplication(attachment_content, _subtype='zip')
attachment_mime.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_file_path))
msg.attach(attachment_mime)

 

# Convert the message to a string
raw_message = msg.as_string()

 

# Send the email with attachment
try:
    response = ses.send_raw_email(
        Source=sender_email,
        Destinations=[recipient_email],
        RawMessage={'Data': raw_message}
    )
    print("Email with attachment sent successfully!")
except NoCredentialsError:
    print("AWS credentials not found, or incorrect.")
except Exception as e:
    print("An error occurred:", str(e))
