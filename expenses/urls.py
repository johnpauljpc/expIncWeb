from django.urls  import path
from .views import index, addExpense

urlpatterns = [
    path('', index, name="index"),
    path("add-expense/", addExpense, name="add-expense")
]
