import re
import threading
from email.policy import default
from re import fullmatch
import phonenumbers
from decouple import config

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError
from twilio.rest import Client

email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
phone_regex = re.compile(r'(\+[0-9]+\s*)?(\([0-9]+\))?[\s0-9\-]+[0-9]+')
username_regex = re.compile(r'(^[a-zA-Z0-9_\-]+$)')


def check_email_or_phone(value):

    # check email
    if email_regex.fullmatch(value):
        return "email"

    # check phone
    try:
        phone_number = phonenumbers.parse(value, None)
        if phonenumbers.is_valid_number(phone_number):
            return "phone"
    except phonenumbers.NumberParseException as e:
        pass

    raise ValidationError("Invalid email or phone number")


def check_user_type(user_input):
    # phone_number = phonenumbers.parse(user_input, None)
    if re.fullmatch(email_regex, user_input):
        user_input = "email"
    elif re.fullmatch(phone_regex, user_input):
        user_input = "phone"
    elif re.fullmatch(username_regex, user_input):
        user_input = "username"
    else:
        raise ValidationError("Invalid username,email or phone number")
    return user_input

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Email:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["subject"],
            body=data["body"],
            from_email=data["from_email"],
            to=[data["to"]],
        )
        if data.get('content_type') == "html":
            email.content_subtype = 'html'
        EmailThread(email).start()

def send_email(email, code):
    html_content = render_to_string(
        'email/authentication/activate_account.html',
        {"code": code},
    )
    Email.send_email(
        {
            "subject": "Registering",
            "to": email,
            "from_email": "<EMAIL>",
            "body": html_content,
            "content_type": "html",
        }
    )


def send_phone_code(phone, code):
    account_sid = config('account_sid')
    auth_token = config('auth_token')
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=f"Your code is {code}",
        from_=phone,
        to=f"{phone}",
    )