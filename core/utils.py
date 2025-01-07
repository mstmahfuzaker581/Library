from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_mail_to_user(subject, user, template_name, context={}):
    message = render_to_string(template_name, context)
    send_mail = EmailMultiAlternatives(subject, "", to=[user.email])
    send_mail.attach_alternative(message, 'text/html')
    send_mail.send()