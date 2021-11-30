from django.core.mail import send_mail
from decouple import config

DOMAIN = config("DOMAIN")

def send_activation_email(email, activation_code, is_password):
    if not is_password:
        activation_url = f'{DOMAIN}/account/activate/{activation_code}'
        message = f"To activate your account click here {activation_url}"
    else:
        activation_url = f'{DOMAIN}/account/forgot_password_complete/{activation_code}'
        message = f"To reset your password click here {activation_url}"

    send_mail('Library Activation', message, 'admin@admin.com', [email, ], fail_silently=False)
