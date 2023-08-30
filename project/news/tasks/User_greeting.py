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