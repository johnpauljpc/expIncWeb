from django.shortcuts import render
from django.views.generic import View

# Create your views here.
class DashboardView(View):
    def get(self, request):
        dashb = 'q'
        context = {
            'dashb':dashb
        }
        return render(request, 'dashboard/dashboard.html', context)
