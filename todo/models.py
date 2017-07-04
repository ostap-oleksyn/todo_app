from django.conf import settings
from django.db import models

# Create your models here.
from django.urls import reverse


class Task(models.Model):
    text = models.CharField(max_length=120)
    done = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def get_absolute_url(self):
        return reverse('todo:edit', kwargs={'pk': self.id})

    class Meta:
        ordering = ['-created']
