from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponse
from django.views.generic import TemplateView
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage

# Create your views here.
class EmailVaidation(View):
    def  post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error':'email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':"Email already taken"}, status=409)
      

        return JsonResponse({'email_valid':True}, status=200)
        


class usernameValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error':'Username should contain only alphanumeric'}, status = 400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Username exists already, choose another'}, status = 409)


        return JsonResponse({'username_valid': True})


class registrationView(View):
    def get(self, request):
        
        return render(request, 'authentication/register.html')
    

    def post(self, request):
        # to create a user:
        #1 Get the data
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        #making the values not lost from the Form field when theres error
        context = {
            'fieldValues':request.POST
        }
        #2 Validate the data
        if User.objects.filter(username = username).exists():
            messages.warning(request, "This Username already exists")
            return render(request, 'authentication/register.html', context)

        if not User.objects.filter(username = username).exists():
            if not User.objects.filter(email = email).exists():
                if (len(password1) < 8):
                    messages.error(request, "password should not be less than 8 characters ")
                    return render(request, 'authentication/register.html', context)
                elif (str(password1).isalnum()):
                    messages.error(request, "password should should contain special characters ")
                    return render(request, 'authentication/register.html', context)
                elif (password1 != password2):
                    messages.error(request, "password does not match")
                    return render(request, 'authentication/register.html', context)
                #3 Create user
                user = User.objects.create_user(username=username, email=email, password=password1)
                #or 
                #user.set_password(password1)
                user.is_active = False
               
                email_subject = "Account Activation"
                email_body = "Your account has been created follow this link to activate your account"
                email_from = "iam.jpcg@gmail.com"
                

                email = EmailMessage(
                    email_subject,
                    email_body,
                    'iam.jpcg@gmail.com',

                    [email],
                )
                email.send(fail_silently=False)

                user.save()
                messages.success(request, "account created")
        
       



       
        return render(request, 'authentication/register.html')