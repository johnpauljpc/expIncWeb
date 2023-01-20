from django.urls import path
from .views import (registrationView, usernameValidation,passwordReset,completePasswordReset,
 EmailVaidation, verificationView, LoginView, LogoutView)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as v


urlpatterns = [
    path('register/', registrationView.as_view(), name='register'),
    path('validate-username/', csrf_exempt(usernameValidation.as_view()), name='validate-username'),
    path('val-email/', csrf_exempt(EmailVaidation.as_view()), name="validate-email"),
    path('login/', LoginView.as_view(), name='login'),
    path('activate/<uidb64>/<token>/', verificationView.as_view(), name="activate"),
    path('logout/', LogoutView.as_view(),  name='logout'), 
    path('reset-password/', passwordReset.as_view(), name="reset-password"), 
    path('set-new-password/<uidb64>/<token>/', completePasswordReset.as_view(),name='set-new-password')
    
]