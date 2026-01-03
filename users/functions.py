import hashlib 
from django.conf import settings
from django.core.mail import send_mail
def generate_hash(str):
    result = hashlib.sha256(str.encode()) 
    return result.hexdigest()





def send_account_activation_email(email,email_token):
    print('sending email to ',email," with token ",email_token)

    subject = "Your accounts needs to be verfied"
    email_from =settings.EMAIL_HOST_USER
    message = f"Hii, click on the link to activate your account http://127.0.0.1:8000/users/verify/{email_token}"
    send_mail(subject,message,email_from,[email])