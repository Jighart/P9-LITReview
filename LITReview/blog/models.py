from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.utils import timezone

from PIL import Image, ImageOps


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(default=timezone.now)
    review_id = models.CharField(blank=True, null=True, max_length=16)
    picture = models.ImageField(blank=True, null=True, upload_to='ticket_pictures')

    def __str__(self):
        return self.title

    IMAGE_MAX_SIZE = (250, 250)

    def resize_image(self):
        if self.picture:
            image = Image.open(self.picture)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            image.save(self.picture.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()




class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline
