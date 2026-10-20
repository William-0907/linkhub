from django.contrib.auth.models import User
from django.db import models

PLATFORM_ICONS = {
    'website': 'fa-globe',
    'youtube': 'fa-youtube',
    'instagram': 'fa-instagram',
    'github': 'fa-github',
    'x': 'fa-x-twitter',
    'twitch': 'fa-twitch',
    'tiktok': 'fa-tiktok',
}

PLATFORM_COLORS = {
    'website': 'text-slate-400',
    'youtube': 'text-red-500',
    'instagram': 'text-pink-500',
    'github': 'text-slate-200',
    'x': 'text-slate-100',
    'twitch': 'text-purple-500',
    'tiktok': 'text-cyan-400',
}


class Link(models.Model):
    PLATFORM_CHOICES = [
        ('website', 'Website'),
        ('youtube', 'YouTube'),
        ('instagram', 'Instagram'),
        ('github', 'GitHub'),
        ('x', 'X (Twitter)'),
        ('twitch', 'Twitch'),
        ('tiktok', 'TikTok'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='links')
    title = models.CharField(max_length=100)
    url = models.URLField()
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='website')
    order = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    @property
    def icon_class(self):
        return PLATFORM_ICONS.get(self.platform, 'fa-globe')

    @property
    def icon_color(self):
        return PLATFORM_COLORS.get(self.platform, 'text-slate-400')


class ClickEvent(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name='click_events')
    referrer = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Click on {self.link.title} at {self.created_at:%Y-%m-%d %H:%M}"
