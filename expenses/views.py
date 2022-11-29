from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "index.html")

def addExpense(request):
    return render(request, "add_expense.html")
