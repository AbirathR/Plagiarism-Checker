from email.mime.text import MIMEText
import smtplib

def send_email(email):
    from_email = "plagiarism.checker83@gmail.com"
    from_password = "eldaas55"
    to_email = email

    subject = "Plagiarism Check"
    message = "Hey there we've checked your request!"

    msg = MIMEText(message,'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email,from_password)
    gmail.send_message(msg)
