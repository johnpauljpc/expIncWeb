from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
import json
from django.http import JsonResponse

# Create your views here.
class usernameValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error':'Username should not contain alphanumeric'}, status = 400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Username exists already, choose another'}, status = 409)


        return JsonResponse({'username_valid': True})


class registrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    