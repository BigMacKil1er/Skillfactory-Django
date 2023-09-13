from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from django.conf import settings

from callboard.models import Advertisement


def send_week_posts(user, posts):
    html_email_message = render_to_string('mail/week_posts_updates.html',
                                          {'username': user, 'posts': posts})
    msg = EmailMultiAlternatives(
        subject='New posts from categories you are subscribed to.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user]
    )
    msg.attach_alternative(html_email_message, 'text/html')
    try:
        msg.send()
    except Exception as e:
        print(e)

def get_week_posts():
    post_for_week = Advertisement.objects.filter(date_creation__gte=timezone.now() - timedelta(days=7))
    users_with_email = [user.email for user in User.objects.exclude(email__isnull=True)]
    print(users_with_email)
    for user_email in users_with_email:
        # user = User.objects.get(email=user_email)
        if user_email:
            print(f'Sent email to ({user_email})')
            send_week_posts(user_email, post_for_week)
            print(f'Sent email to  ({user_email})')