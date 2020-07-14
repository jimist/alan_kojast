from django.db import models


class GuestTokens(models.Model):
    token = models.CharField(max_length=127)
    waiting = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

