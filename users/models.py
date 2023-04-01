from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import os

# Currency
class Currency(models.Model):
    currency_name = models.CharField(max_length=50)
    currency_short_name = models.CharField(max_length=10)
    currency_symbol = models.CharField(max_length=10)
    currency_price = models.FloatField()

    def __str__(self):
        return self.currency_short_name

class CustomUser(AbstractUser):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join("Users", self.username, instance)
        return None

    STATUS = (
        ('regular', 'regular'),
        ('subscriber', 'subscriber'),
        ('moderator', 'moderator'),
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='regular')
    description = models.TextField("Description", max_length=600, default='', blank=True)
    image = models.ImageField(default='default/user.jpg', upload_to=image_upload_to)
    currency = models.ForeignKey(Currency, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class SubscribedUsers(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    created_date = models.DateTimeField('Date created', default=timezone.now)

    def __str__(self):
        return self.email
