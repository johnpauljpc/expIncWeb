from django.urls  import path
from .views import index, addExpense, updateExpense,deleteExpense

urlpatterns = [
    path('', index.as_view(), name="expenses"),
    path("add-expense/", addExpense, name="add-expense"),
    path("edit/<int:id>/", updateExpense, name='update-expense'),
    path("delete/<int:id>/", deleteExpense, name='delete-expense'),

]
