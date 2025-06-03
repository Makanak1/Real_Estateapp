from django.core.mail import send_mail
from django.conf import settings

def send_Email(email):
    subject = "Welcome on-board"
    body = ''''
        Dear User,
        Thank you for registering with us. We are excited to have you on board.
    
    '''
    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )