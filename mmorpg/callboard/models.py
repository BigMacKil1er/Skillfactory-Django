from django.db import models
from django.contrib.auth.models import User

class UserBoard(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.author.username.title()}'
# class UserSubscriber(models.Model):
#     user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
#     category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)

# class Category(models.Model):
#     name = models.CharField(max_length=64, unique=True)
#     subscribers = models.ManyToManyField(UserBoard, through=UserSubscriber, blank=True)
#     def __str__(self):
#         return self.name

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
    user = instance.advertisement.user

    # Генерируем путь для сохранения файла: media_content/имя_пользователя/имя_файла
    return f'media_content/{user}/{filename}'

# Модель для медиа-контента в объявлениях
class MediaContent(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    media_type_choices = [
        ('image', 'Изображение'),
        ('video', 'Видео'),
        ('other', 'Другое'),
    ]
    media_type = models.CharField(max_length=10, choices=media_type_choices)
    file = models.FileField(upload_to=user_directory_path)

class UserResponse(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    user = models.ForeignKey(UserBoard, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
