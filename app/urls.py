from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
    path("detect/", detect_waste, name="detect_waste"),
    path("", lambda request: redirect("login"), name="home"),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/public/', public_dashboard, name='public_dashboard'),
    path("upload_garbage/", upload_garbage, name="upload_garbage"),
    path('upload/', upload_image, name='upload_image'),

    path("city-manager/", city_manager_view, name="city_manager"),
    path("image/<int:image_id>/", image_detail_view, name="image_detail"),
    path("image/<int:image_id>/delete/", delete_image, name="delete_image"),

]
