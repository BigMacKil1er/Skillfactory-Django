from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import PostCategory, Post
from news.tasks import news_post_subscription

@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        news_post_subscription(instance)
        pass