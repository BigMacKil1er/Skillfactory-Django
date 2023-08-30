from news.models import Post
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from django.conf import settings


def send_week_posts(user, posts):
    html_email_message = render_to_string('mail/week_posts_updates.html',
                                          {'username': user.username, 'posts': posts})
    msg = EmailMultiAlternatives(
        subject='New posts from categories you are subscribed to.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    msg.attach_alternative(html_email_message, 'text/html')
    try:
        msg.send()
    except Exception as e:
        print(e)

def get_week_posts():
    post_for_week = Post.objects.filter(dateCreation__gte=timezone.now()-timedelta(days=7))
    post_for_week_users = {}
    for post in post_for_week:
        for category in post.postCategory.all():
            for user in category.subscribers.all():
                if user in post_for_week_users.keys() and post not in post_for_week_users[user]:
                    post_for_week_users[user].append(post)
                else:
                    post_for_week_users[user] = [post]
    for user, posts in post_for_week_users.items():
        send_week_posts(user, posts)
        print('Done')