from django.urls  import path
from .views import index, addExpense

urlpatterns = [
    path('', index.as_view(), name="expenses"),
    path("add-expense/", addExpense, name="add-expense")
]
