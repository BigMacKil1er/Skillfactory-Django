from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def greeting(user):
    username = user.username
    html_email_message = render_to_string('mail/greeting.html',
                                          {'username': username})
    subject = f'Greetings, {username}.'
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    msg.attach_alternative(html_email_message, 'text/html')
    try:
        msg.send()
    except Exception as e:
        print(e)

def send_confirmation_email(email, confirmation_code):
    html_email_message = render_to_string('mail/confirm.html',
                                          {'confirmation_code': confirmation_code})
    subject = f'Сonfirm registration'
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email]
    )
    msg.attach_alternative(html_email_message, 'text/html')
    try:
        msg.send()
    except Exception as e:
        print(e)

def send_response_email(email):
    html_email_message = render_to_string('mail/email_succes_response.html')
    subject = f'Ваш отклик был принят'
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email]
    )
    msg.attach_alternative(html_email_message, 'text/html')
    try:
        msg.send()
    except Exception as e:
        print(e)

def send_response_for_author_email(email):
    html_email_message = render_to_string('mail/email_for_author_response.html')
    subject = f'На ваше Объявление откликнулись'
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email]
    )
    msg.attach_alternative(html_email_message, 'text/html')
    try:
        msg.send()
    except Exception as e:
        print(e)