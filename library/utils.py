from django.core.mail import send_mail
from decouple import config


def send_email(email, message):
    send_mail('INAI Library', message, 'admin@admin.com', [email, ], fail_silently=False)
