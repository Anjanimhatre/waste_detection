from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

CITY_CHOICES=[
        ("Mumbai","Mumbai"),
        ("Delhi", "Delhi"),
        ("Bangalore", "Bangalore"),
        ("Kolkata", "Kolkata"),
        ("Chennai", "Chennai"),
        ("Hyderabad", "Hyderabad"),
        ("Pune", "Pune"),
        ("Ahmedabad", "Ahmedabad"),
        ("Jaipur", "Jaipur"),
        ("Lucknow", "Lucknow"),
    ]
class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.USER_TYPES, label="User Type")
   
    city=forms.ChoiceField(choices=CITY_CHOICES,label="city",required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role','city', 'password1', 'password2']

class WasteImageForm(forms.ModelForm):
    class Meta:
        model = WasteImage
        fields = ["image"]
#for public user
class UploadForm(forms.ModelForm):
    city=forms.ChoiceField(choices=CITY_CHOICES)
    class Meta:
        model = UploadedImage
        fields = ["image", "location","city"]
#for city manager

class CleanedImageForm(forms.ModelForm):
    class Meta:
        model = UploadedGarbage
        fields = ["cleaned_image"]
class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ["image", "location"]
class GarbageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedGarbage
        fields = ('image', 'location','city')