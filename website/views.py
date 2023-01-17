from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

class test(View):
    def get(self, *args, **kwargs):
        return HttpResponse("hello")