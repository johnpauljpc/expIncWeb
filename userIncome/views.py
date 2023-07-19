from django.shortcuts import render, redirect
from django.contrib.auth import decorators
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from .models import Income, Source
from django.contrib import messages
from django.utils.timezone import now
from django.http import HttpResponse, JsonResponse
import pdb
from django.core.paginator import Paginator
import json
from userPrefrences.models import userPrefrences
from django.db.models import Q

def searchIncome(request):
    
    if request.method == 'POST':
        query = json.loads(request.body).get('searchText')
        print('*************************  ',query,'  *****************************')

        # income = Expense.objects.filter(amount__istartswith = search_str, owner = request.user)\
        #     |Expense.objects.filter(date__istartswith = search_str, owner = request.user)\
        #        | Expense.objects.filter(description__istartswith = search_str, owner = request.user) \
        #             | Expense.objects.filter(category__istartswith = search_str, owner = request.user)
        income = Income.objects.filter(Q(amount__icontains=query, user=request.user) \
            |Q(description__icontains=query, user=request.user)|Q(source__icontains=query, user=request.user)|Q(date__icontains=query, user=request.user))

        data = income.values()
        return JsonResponse(list(data), safe=False)
    return render(request, 'income/index.html')




# Create your views here.
#@decorators.login_required(login_url = "login")
# def index(request):
#     return render(request, "index.html")

class index(LoginRequiredMixin,TemplateView):
    def get(self, request):
        income = Income.objects.filter(user=request.user)
        source = Source.objects.all()
        try:
            currency = userPrefrences.objects.get(user=request.user).currency
        except Exception as e:
            messages.error(request, f'{e} >>  So, please select your\n preffered currency ')
            return redirect('preference')
        
        

        paginator = Paginator(income, 6)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)


        context = {'incomes':income, 'source':source,
        'page_obj':page_obj, 'currency':currency}
        return render(request, 'income/index.html', context)

def addIncome(request):
    source = Source.objects.all()
    values = request.POST
    context = { 'values':values, 'source':source}

    if request.method == 'POST':
        amount = request.POST['amount']
        date = request.POST['date']
        description = request.POST['description']
        source = request.POST['source']

        if not amount:
            messages.info(request, "amount is required!")
            return render(request, "income/add_income.html", context)
        elif not description:
            messages.info(request, "description is required!")
            return render(request, "income/add_income.html", context)
        elif not date:
            messages.info(request, "date is required!")
            return render(request, "income/add_income.html", context)
        
        else:
            Income.objects.create(amount=amount, date=date, description=description, user = request.user, source=source)
            messages.success(request, "Just added a new record!")
            return redirect('income')


    return render(request, "income/add_income.html", context)


def addSource(request):


    if request.method == 'POST':
        source = request.POST['name']
        Source.objects.create(name=source)
        messages.info(request, "A new source added")
        return redirect('income')

        
    return render(request, 'income/add_Source.html')
    
@decorators.login_required(login_url='/auth/login/')
def updateIncome(request, id):
    income = Income.objects.get(pk=id)
    source = Source.objects.all()
    
    
    context = {'source':source, 'income':income}

    if request.method == 'POST':
        amount = request.POST['amount']
        date = request.POST['date']
        description = request.POST['description']
        source = request.POST['source']
        
        
        

        income.owner = request.user
        income.amount = amount
        income.date = date
        income.description = description
        income.source = source
        
       
        # print('****   ',category, '   *****')
        # pdb.set_trace()
        income.save()

        messages.success(request, "Successfully Updated record!")
        return redirect('income')
        

    return render(request, "income/edit_income.html", context)


@decorators.login_required(login_url='/auth/login/')
def deleteIncome(request, id):
    print("****************************************************")
    print(request)
    print(id)
    income = Income.objects.get(pk=id)
    income.delete()
    messages.info(request, f"{income.description} deleted")
    return redirect('income')
