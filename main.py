import smtplib #To connect to SMTP(Simple Message Transfer Protocol) server to be able to send emails
import ssl #To make the connection SMTP server secured

import csv #To retrieve email from csv file

from email import encoders #To encode the attachment to our email into Base64
from email.mime.base import MIMEBase #Lets us attach a file, such as pdf, audio, video, image or more to our email
from email.mime.multipart import MIMEMultipart #Lets us to construct a complex email, that can contain plain text, html parts or/and file attachments
from email.mime.text import MIMEText #Constructs the subject and text body part of the email

#Setting up the server and port we will need to connect, in our case Gmail
server = "smtp.gmail.com"
port = 465

#Setting up the email we will use, password and email subject
#NOTE: emailPassword here is not the password you use to log into your email, please read "readme" file to understand what password to use
emailSender = "sender@gmail.com"
emailPassword = "your password"

emailSubject = "New Task"

#Specifyin our csv file name and pdf file name
#NOTE: Attachment to email can be also image, audio or video

csvFile = "employee.csv"
pdfFile = "NewTask.pdf"

#opening our csv file to retrieve employees info
with open(csvFile) as file:
    reader = csv.reader(file)
    next(reader) #skipping the head of the csv file

    for name, email in reader:
        emailReciever = email
        emailBody = f"""
        Hello, {name}!
        We have a new task today!
        Please, get familiar with the task in the pdf file attached.
        Best Regards!
        """

        #We are creating an instance of the MIMEMultipart and constructing the email we are going to send
        message = MIMEMultipart()
        message["To"] = emailReciever
        message["From"] = emailSender
        message["Subject"] = emailSubject

        message.attach(MIMEText(emailBody, "plain")) #"plain" means our emailBody is plain text, if emailBody was html content, it would have been "html"

        with open(pdfFile, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        #encoding the attachment part to base64, it is essantial to construct an email
        encoders.encode_base64(part)

        #Setting up the header to tell the server that we are attaching a file
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {pdfFile}"
        )

        message.attach(part)

        #Creating secured SMTP server connection, logging into the email we are using and finally sending an email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(server, port, context=context) as host:
            host.login(emailSender, emailPassword)
            host.sendmail(emailSender, emailReciever, message.as_string())