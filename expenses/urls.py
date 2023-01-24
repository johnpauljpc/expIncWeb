from django.urls  import path
from .views import (index, addExpense, updateExpense,deleteExpense, searchExpense,
 expense_category_summary, stats, export_csv, export_excel, export_pdf)
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', index.as_view(), name="expenses"),
    path("add-expense/", addExpense, name="add-expense"),
    path("edit/<int:id>/", updateExpense, name='update-expense'),
    path("delete/<int:id>/", deleteExpense, name='delete-expense'),
    path("search-expense/", csrf_exempt(searchExpense), name='search-expense'),
    path("expense-summary/", expense_category_summary, name='expense_category_summary'),
    path("stats/", stats, name='stats'),
    path('to-csv/', export_csv, name='export_csv'),
    path('to-excel/', export_excel, name='export_excel'),
    path('to-pdf/', export_pdf, name='export_pdf')


]
