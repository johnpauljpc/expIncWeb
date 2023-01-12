from django.shortcuts import render, redirect
from django.contrib.auth import decorators
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from .models import Expense, Category
from django.contrib import messages
from django.utils.timezone import now
from django.http import HttpResponse
import pdb




# Create your views here.
#@decorators.login_required(login_url = "login")
# def index(request):
#     return render(request, "index.html")

class index(LoginRequiredMixin,TemplateView):
    def get(self, request):
        expense = Expense.objects.filter(owner=request.user)
        category = Category.objects.all()
        context = {'expenses':expense, 'category':category}
        return render(request, 'index.html', context)

def addExpense(request):
    category = Category.objects.all()
    values = request.POST
    context = { 'values':values, 'category':category}

    if request.method == 'POST':
        amount = request.POST['amount']
        date = request.POST['date']
        description = request.POST['description']
        category = request.POST['category']

        if not amount:
            messages.info(request, "amount is required!")
            return render(request, "add_expense.html", context)
        elif not description:
            messages.info(request, "description is required!")
            return render(request, "add_expense.html", context)
        elif not date:
            messages.info(request, "date is required!")
            return render(request, "add_expense.html", context)
        
        else:
            Expense.objects.create(amount=amount, date=date, description=description, owner = request.user, category=category)
            messages.success(request, "Successfully added an expense!")
            return redirect('expenses')


    return render(request, "add_expense.html", context)



def updateExpense(request, id):
    expense = Expense.objects.get(pk=id)
    category = Category.objects.all()
    
    context = {'expense':expense, 'category':category}

    if request.method == 'POST':
        amount = request.POST['amount']
        date = request.POST['date']
        description = request.POST['description']
        category = request.POST['category']

        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.description = description
        expense.category = category
        
       
        # print('****   ',category, '   *****')
        # pdb.set_trace()
        expense.save()

        messages.success(request, "Successfully Updates an expense!")
        return redirect('expenses')
        

    return render(request, "edit_expense.html", context)


def deleteExpense(request, id):
    print("****************************************************")
    print(request)
    print(id)
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.info(request, f"{expense.description} deleted")
    return redirect('expenses')
