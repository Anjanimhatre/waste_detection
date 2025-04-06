from django.shortcuts import render, redirect,get_object_or_404, redirect
from django.contrib.auth import login, logout
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import numpy as np
from django.shortcuts import render
from django.core.files.storage import default_storage
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input
from PIL import Image
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.city=form.cleaned_data['city']
            user.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect based on user role
            if user.role == 'city_manager':
                return redirect('city_manager')  # Change to your actual URL name
            else:
                return redirect('public_dashboard')  # Change to your actual URL name

    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        if request.user.role == 'city_manager':
            return render(request, 'city_manager_dashboard.html')  # Correct template path
        else:
            return render(request, 'public_dashboard.html')  # Correct template path
    return redirect('login')
    
@login_required
def public_dashboard(request):
    return render(request, 'public_dashboard.html')

@login_required
def detect_garbage(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Process the uploaded image (Placeholder)
        return JsonResponse({'message': 'Garbage detected successfully!', 'status': 'success'})

    return render(request, 'detect_garbage.html')
@login_required
def upload_garbage(request):
    if request.method == "POST":
        form = GarbageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save(commit=False)
            uploaded_image.user = request.user  # Assign logged-in user
            uploaded_image.city=form.cleaned_data['city']
            uploaded_image.save()


            # Get user email
            user_email = request.user.email  # Email of the user uploading the image
            admin_email = settings.ADMIN_EMAIL  # Your admin email (set in settings.py)
            image_file = uploaded_image.image.path  # Get image path

            # Email setup
            email_subject = "New Garbage Upload"
            email_body = f"A new garbage image has been uploaded.\n\nLocation: {uploaded_image.location}\nUser: {user_email}"

            # Attach image
            email = EmailMessage(email_subject, email_body, user_email, [admin_email])
            email.attach_file(image_file)  # Attach the uploaded image
            email.send()

            # Success message (no redirect to reward page as per your request)
            messages.success(request, "Image uploaded successfully!")

            return redirect("upload_garbage")  # Reload the upload page

    else:
        form = GarbageUploadForm()
    
    return render(request, "upload.html", {"form": form})


# Load the trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../personal/model_checkpoint.keras")
model = load_model(MODEL_PATH)

def preprocess_image(image):
    """ Preprocess uploaded image for model input """
    image = image.resize((150, 150))  # Resize to model input size
    image = np.array(image)  # Convert to numpy array
    image = preprocess_input(image)  # Apply preprocessing
    image = np.expand_dims(image, axis=0)  # Expand dimensions for batch input
    return image

def detect_waste(request):
    """ Django view for waste detection """
    prediction = None
    category = None
    confidence = None
    image_url = None  # Store image URL for display

    if request.method == "POST" and request.FILES.get("waste_image"):
        uploaded_file = request.FILES["waste_image"]
        file_path = default_storage.save("uploaded_images/" + uploaded_file.name, uploaded_file)
        file_path = default_storage.path(file_path)  # ✅ Fix: Convert to absolute path

        # Get URL for displaying the image
        image_url = default_storage.url(file_path)

        # Open image and process it
        image = Image.open(file_path)
        processed_image = preprocess_image(image)

        # Predict using the model
        prediction = model.predict(processed_image)[0][0]

        # Determine category
        category = "Organic Waste" if prediction < 0.5 else "Recyclable Waste"
        confidence = round((1 - prediction) * 100 if prediction < 0.5 else prediction * 100, 2)

    return render(request, "detect_garbage.html", {
        "category": category, 
        "confidence": confidence,
        "image_url": image_url  # Pass image URL to template
    })
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from .models import *
from .forms import UploadForm
import os

def upload_image(request):
    images = UploadedGarbage.objects.all()
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save(commit=False)
            uploaded_image.user = request.user  # Get the logged-in user
            uploaded_image.save()

            # Get user & admin email
            admin_email = "anjanimhatre28@gmail.com"
            user_email = request.user.email  # Get the logged-in user's email

            # Get the image path
            image_file = uploaded_image.image
            image_path = image_file.path

            # Compose email with attachment including user email
            email_subject = "New Image Upload by User"
            email_body = (
                f"User Email: {user_email}\n"
                f"City: {uploaded_image.city}\n"
                f"Location: {uploaded_image.location}\n\n"
                f"Find the attached image."
            )

            email = EmailMessage(
                email_subject, email_body, from_email="anjanimhatre28@example.com", to=[admin_email]
            )

            # Attach the image
            if os.path.exists(image_path):  # Ensure file exists
                email.attach_file(image_path)

            # Send the email
            email.send()

            messages.success(request, "Image uploaded successfully!")

    else:
        form = UploadForm()

    return render(request, "upload.html", {"form": form})

@login_required
def city_manager_view(request):
    if request.user.role != 'city_manager':
        return redirect("public_dashboard")  # Restrict non-managers

    city_name = str(request.user.city)  # Convert city object to string
    images = UploadedGarbage.objects.filter(city=city_name)

    print("Filtering images for city:", city_name)  # Debugging statement

    return render(request, "city_manager.html", {"images": images})

@login_required
def image_detail_view(request, image_id):
    image = get_object_or_404(UploadedGarbage, id=image_id)

    if request.method == "POST":
        form = CleanedImageForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_image = form.cleaned_data["cleaned_image"]
            image.cleaned_image = cleaned_image
            image.cleaned_by = request.user  # Assign the city manager who cleaned it
            image.save()
            messages.success(request, "Cleaned image uploaded successfully!")
            return redirect("city_manager")
    else:
        form = CleanedImageForm()

    return render(request, "image_detail.html", {"image": image, "form": form})

@login_required
def delete_image(request, image_id):
    image = get_object_or_404(UploadedGarbage, id=image_id)
    image.delete()
    messages.success(request, "Image deleted successfully!")
    return redirect("city_manager")