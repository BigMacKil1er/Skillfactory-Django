from django.db import models
from django.contrib.auth.models import User

class UserBoard(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.author.username.title()}'

class Advertisement(models.Model):
    author = models.ForeignKey(UserBoard, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    text = models.TextField()
    category_choices = [
        ('Танки', 'Танки'),
        ('Хилы', 'Хилы'),
        ('ДД', 'ДД'),
        ('Торговцы', 'Торговцы'),
        ('Гилдмастеры', 'Гилдмастеры'),
        ('Квестгиверы', 'Квестгиверы'),
        ('Кузнецы', 'Кузнецы'),
        ('Кожевники', 'Кожевники'),
        ('Зельевары', 'Зельевары'),
        ('Мастера заклинаний', 'Мастера заклинаний'),
    ]
    category = models.CharField(max_length=20, choices=category_choices)
    date_creation = models.DateTimeField(auto_now_add=True)

def user_directory_path(instance, filename):
    user = instance.advertisement.author
    return f'media_content/{user}/{filename}'

class MediaContent(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    media_type_choices = [
        ('image', 'Изображение'),
        ('video', 'Видео'),
        ('other', 'Другое'),
    ]
    media_type = models.CharField(max_length=10, choices=media_type_choices)
    media_file = models.FileField(upload_to=user_directory_path)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_media_type_display()} for {self.advertisement.title}"

class UserResponse(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    user = models.ForeignKey(UserBoard, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
