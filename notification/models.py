from django.db import models
from django.conf import settings
from shop.models import Shop


class Notification(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='notifications')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} in {self.shop.name}"
