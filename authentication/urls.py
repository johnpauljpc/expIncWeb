from django.urls import path
from .views import registrationView

urlpatterns = [
    path('register/', registrationView.as_view(), name='register')
]