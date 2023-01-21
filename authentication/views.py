from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponse
from django.views.generic import TemplateView
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.contrib.auth import authenticate, login, logout, decorators
from django.contrib.auth.tokens import PasswordResetTokenGenerator



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

                #path to view
                #--- getting domain we are in
                #--- relative url to verification
                #--- encoded uid
                #--- token

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                #if 'first line'.encode('utf-8') in result[0]:
                domain =  get_current_site(request).domain
                link = reverse("activate", kwargs={
                    'uidb64':uidb64, 'token':token_generator.make_token(user)})
                print("************************** Domain ************************")
                print(domain)
                print("************************** Link ************************")
                print(link)


                activate_url = 'http://'+domain+link
               
                email_subject = "Account Activation"
                email_body = "Hi" + user.username + "Your account has been created follow the link below to verify and activate your account\n\
                "+ activate_url
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
       



       
        return render(request, 'authentication/register.html')

class verificationView(View):
    def get(self, request, uidb64, token):

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            print("************************  ID ********************")
            print(id)
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login'+ '?message=' +'User already activated')


            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass



        return redirect("login")


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html') 

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password1']

        if username and password:
            user = authenticate(username=username, password=password)
            
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'welcome  ' + user.username + ' You are now logged in')
                    return redirect('expenses')
            
                messages.error(request, 'Your account is not active, please check your email')
                return render(request, 'authentication/login.html')

            messages.error(request, 'Your credentials are invalid, try again')
            return render(request, 'authentication/login.html')
        
        messages.warning(request, "Please fill all fields")
        return render(request, 'authentication/login.html')
    
    
# class LogoutView(View):
    
#     # def get(self, request):
#     #     return render(request, "authentication/logout.html")


class LogoutView(View):
    def get(self, request):
        return render(request, 'authentication/logout.html')
    def post(self, request):
        logout(request)
        messages.info(request, "You have been logged out")
        return render(request, 'authentication/logout.html')

class passwordReset(View):
    

    def get(self, request):
        return render(request, "authentication/reset_password.html")

    def post(self, request):
        email = request.POST['email']
        fieldValue = email
        context = {'fieldValue':fieldValue}
        if not validate_email(email):
            messages.error(request, "email is not valid")
        elif not User.objects.filter(email=email).exists():
            messages.warning(request, "email is not registered with us")
            return render(request, 'authentication/reset_password.html', context)

        
        current_site =  get_current_site(request)
        user = User.objects.filter(email=email)
        #or user = request.objects.filter(email=email).exists()

        if user.exists():
            email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user[0].id)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),

            }
            print("*********** Email Contents *******ID*********")
            print(email_contents)
            link = reverse('set-new-password', kwargs={
                'uidb64':email_contents['uid'], 'token':email_contents['token']
            })
            email_subject = 'PassWord Reset Instructions'
            reset_url ='http://'+current_site.domain+link 

            email = EmailMessage(
                email_subject,
                'Hi there, please follow the link below to reset your password\n'+ reset_url,
                'noreply@semicolon.com',
                [email]
            )
            email.send(fail_silently=False)

        messages.success(request, "we have sent a reset link to your email")



        return render(request, 'authentication/reset_password.html', context)


class completePasswordReset(View):

    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
            
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, "password reset  link is invalid, please request for a new one")
                
                return render(request, 'authentication/reset_password.html', context) 
        except Exception as e:
            pass
            
        return render(request, 'authentication/set-new-password.html', context)

    def post(self, request, uidb64, token):
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
        context = {
            'uidb64': uidb64,
            'token': token,
            
        }
        if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, "password reset  link is invalid, please request for a new one")
                
                return render(request, 'authentication/reset_password.html', context) 
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        if (pass1 != pass2):
            messages.error(request, "password doesn't match!")
            return render(request, 'authentication/set-new-password.html', context)
        if len(pass1) < 6:
            messages.error(request, "password too short! should be atleast 6 characters")
            return render(request, 'authentication/set-new-password.html', context)
        if (str(pass1)).isalnum() or (str(pass2)).isalnum(): 
            messages.error(request, "password must have a special character")
            return render(request, 'authentication/set-new-password.html', context)
        
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            user.set_password(pass1)
            user.save()
           
            messages.success(request, "Password changed successfully, You can now login with your new password")
            return redirect('login')
        except Exception as e:
            messages.info(request, 'something went wrong, please try again')
            return render(request, 'authentication/set-new-password.html', context)
    
        

