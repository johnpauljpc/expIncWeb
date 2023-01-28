from django.shortcuts import render, redirect
from django.contrib.auth import decorators
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from .models import Expense, Category
from django.contrib import messages
from django.utils.timezone import now
from django.http import HttpResponse, JsonResponse
import pdb
from django.views import View
from django.core.paginator import Paginator
import json
from userPrefrences.models import userPrefrences
import datetime
import csv
import xlwt

#modules for pdf generation
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from django.db.models import Sum


def searchExpense(request):
    
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expense = Expense.objects.filter(amount__icontains = search_str, owner = request.user)\
            |Expense.objects.filter(date__icontains = search_str, owner = request.user)\
               | Expense.objects.filter(description__icontains = search_str, owner = request.user) \
                    | Expense.objects.filter(category__icontains = search_str, owner = request.user)

        data = expense.values()
        return JsonResponse(list(data), safe=False)
    return HttpResponse("Hello")




# Create your views here.
#@decorators.login_required(login_url = "login")
# def index(request):
#     return render(request, "index.html")

class index(LoginRequiredMixin,TemplateView):
    def get(self, request):
        expense = Expense.objects.filter(owner=request.user)
        category = Category.objects.all()
        try:
            currency = userPrefrences.objects.get(user=request.user).currency
        except:
            currency = None

        paginator = Paginator(expense, 4)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)


        context = {'expenses':expense, 'category':category,
        'page_obj':page_obj, 'currency':currency}
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

        messages.success(request, "Successfully Updated an expense!")
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

def expense_category_summary(request):
    todays_date = datetime.date.today()
    last_six_months = todays_date - datetime.timedelta(30*6)

    expense = Expense.objects.filter(owner= request.user, date__gte = last_six_months, date__lte = todays_date)

    finalrep = {}

    def get_category(expense):
        return expense.category

    category_list = list(set(map(get_category, expense)))

    def get_expense_category_amount(category):
        amount = 0

        filtered_category = expense.filter(category=category)
        for item in filtered_category:
            amount += item.amount
        return amount

    for x in expense:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats(request):
    
    return render(request, 'partials/stats.html')


def export_csv(request):
    
    response = HttpResponse(content_type = "text/csv")
    response['Content-Disposition'] = 'attachment; filename='+str(request.user)+'_expense_'+str(datetime.date.today())+'.csv'

    writer = csv.writer(response)

    writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    expense = Expense.objects.filter(owner = request.user)

    for ex in expense:
        writer.writerow([ex.amount, ex.description, ex.category,ex.date])


    return response


def export_excel(request):
    response = HttpResponse(content_type ='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename='+str(request.user)+ '_expenses_'+ str(datetime.date.today())+'.xls'

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Amount', 'Description', 'Category', 'Date']


    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = Expense.objects.filter(owner = request.user).values_list('amount', 'description', 'category', 'date', )


    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(columns[col_num]), font_style)

    wb.save(response)

    return response




# def export_pdf(request):
#     expense = Expense.objects.filter(owner = request.user)




def export_pdf(request):
    template_path = 'pdf-output.html'
    expense = Expense.objects.filter(owner = request.user)
    sum = expense.aggregate(Sum('amount'))
    user = request.user
    
    
    try:
        currency = userPrefrences.objects.get(user = request.user).currency
    except:
        currency = None
    context = {'expense':expense, 'currency':currency, 'user':user, 'total':sum['amount__sum']}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' +str(user)+'_expense_'+str(datetime.date.today())+ '.pdf'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

