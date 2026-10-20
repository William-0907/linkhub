from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    BG_STYLE_CHOICES = [
        ('dark', 'Midnight'),
        ('aurora', 'Aurora'),
        ('sunset', 'Sunset'),
        ('ocean', 'Ocean'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    accent_color = models.CharField(max_length=7, default='#6366f1')
    bg_style = models.CharField(max_length=10, choices=BG_STYLE_CHOICES, default='dark')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
