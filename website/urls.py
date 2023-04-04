
from django.contrib import admin
from django.urls import path, include
from .views import test

urlpatterns = [
    path('', include('expenses.urls')),
    path('', include('dashboard.urls')),
    path('income/', include('userIncome.urls')),

    path('preference/', include("userPrefrences.urls")),
    path('auth/', include("authentication.urls")),
    path('admin/', admin.site.urls),
    path('hi/', test.as_view())
]
