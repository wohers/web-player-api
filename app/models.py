from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    email = models.CharField(unique=True)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    username = models.CharField(unique=False, max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'second_name']

    def __str__(self):
        return self.email


class Track(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='tracks/')
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)
    duration = models.IntegerField(default=0, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.artist}"



User = get_user_model()

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    tracks = models.ManyToManyField('Track', through='FavoriteTrack')

    class Meta:
        unique_together = ('user',)

class FavoriteTrack(models.Model):
    favorite = models.ForeignKey(
        Favorite,
        on_delete=models.CASCADE,
        related_name='favoritetrack_set'
    )
    track = models.ForeignKey(
        'Track',
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    added_at = models.DateTimeField(auto_now_add=True)


class Heroes(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=400)
    photo = models.ImageField(upload_to='heroes_photo/', null=True, blank=True)
    map = models.ImageField(upload_to='heroes_map/', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"