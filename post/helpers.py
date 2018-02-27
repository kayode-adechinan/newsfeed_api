# sendgrid tutorial
import sendgrid
from sendgrid.helpers.mail import *
import string
import random


def send_password_reset_mail(email, password):
    API_KEY = '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'
    # create a client
    sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
    # setting up  sender
    from_email = Email("cryts@lab.com")
    # setting up recipiender
    to_email = Email(email)
    # making subject
    subject = "Password"
    # making content
    content = Content("text/plain", password)
    # sending mail and get response
    mail = Mail(from_email, subject, to_email, content)

    sg.client.mail.send.post(request_body=mail.get())


def generate_user_password():
    min_char = 8
    max_char = 12
    allchar = string.ascii_letters + string.digits
    password = "".join(random.choice(allchar) for x in range(random.randint(min_char, max_char)))
    return password