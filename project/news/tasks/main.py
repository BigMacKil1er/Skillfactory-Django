from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings

def get_subscriber(category):
    user_email = []
    for user in category.subscribers.all():
        user_email.append(user.email)
    return user_email

def news_post_subscription(instance):
    template = 'mail/new_post.html'
    for category in instance.postCategory.all():
        email_subject = f'New post in category: {category}'
        user_emails = get_subscriber(category)

        html = render_to_string(
            template_name=template,
            context = {
                'category': category,
                'post': instance
            }
        )
        print(html)
        msg = EmailMultiAlternatives(
            subject=email_subject,
            body='',
            from_email= settings.DEFAULT_FROM_EMAIL,
            to=user_emails
        )
        print(user_emails)
        print(msg)
        msg.attach_alternative(html, 'text/html')
        msg.send()