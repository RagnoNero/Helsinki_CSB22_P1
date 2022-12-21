from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Note(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('title',)