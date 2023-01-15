from django.urls  import path
from .views import index, addIncome, updateIncome,deleteIncome, searchIncome,addSource
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', index.as_view(), name="income"),
    path("add-income/", addIncome, name="add-income"),
    path("add-source/", addSource, name="add-source"),
    path("edit/<int:id>/", updateIncome, name='update-income'),
    path("delete/<int:id>/", deleteIncome, name='delete-income'),
    path("search-income/", csrf_exempt(searchIncome), name='search-income'),


]
