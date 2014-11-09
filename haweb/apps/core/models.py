from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    photo = models.ImageField(upload_to='users', blank=True, null=True)
    title = models.CharField(max_length=250)
    edit_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.edit_date = timezone.now()
        super(UserProfile, self).save(*args, **kwargs)




