from django.urls import path
from .views import registrationView, usernameValidation, EmailVaidation
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', registrationView.as_view(), name='register'),
    path('validate-username/', csrf_exempt(usernameValidation.as_view()), name='validate-username'),
    path('val-email/', csrf_exempt(EmailVaidation.as_view()), name="validate-email"),

]