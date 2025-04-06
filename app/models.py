from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('public', 'Public User'),
        ('city_manager', 'City Manager'),
    )

    role = models.CharField(max_length=20, choices=USER_TYPES, default='public')
    city = models.CharField(max_length=100, blank=False, null=False)  # City as a simple CharField

    def __str__(self):
        return f"{self.username} ({self.get_role_display()} - {self.city})"

class WasteImage(models.Model):
    image = models.ImageField(upload_to="waste_images/")
    predicted_class = models.CharField(max_length=50, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


# for public user
from django.conf import settings  

class UploadedImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
    location = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    cleaned_image = models.ImageField(upload_to="cleaned/", null=True, blank=True)
    cleaned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, blank=True, 
        on_delete=models.SET_NULL, 
        related_name="cleaned_images_uploaded"
    )  # Changed related_name to avoid clash

    def __str__(self):
        return f"{self.user.username} - {self.location} ({self.city})"

class UploadedGarbage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploaded_images/")
    location = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=False, null=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    cleaned_image = models.ImageField(upload_to="cleaned/", blank=True, null=True)
    cleaned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name="cleaned_images_garbage"
    )  # Changed related_name to avoid clash

    def __str__(self):
        return f"Garbage uploaded by {self.user.username} in {self.city}"