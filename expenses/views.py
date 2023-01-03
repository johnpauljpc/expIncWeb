from django.shortcuts import render
from django.contrib.auth import decorators
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView




# Create your views here.
#@decorators.login_required(login_url = "login")
# def index(request):
#     return render(request, "index.html")

class index(LoginRequiredMixin,TemplateView):
    def get(self, request):
        return render(request, 'index.html')

def addExpense(request):
    return render(request, "add_expense.html")
