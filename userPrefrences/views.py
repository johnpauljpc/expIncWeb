from django.shortcuts import render
import os
import json
from django.conf import settings
import pdb
from .models import userPrefrences
from django.contrib import messages

# Create your views here.
def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    #pdb.set_trace()
        #COnvert currencies.json to dictionary
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        
    #after converting it to dictionary, convert it to list[array]
        for k,v in data.items():
            currency_data.append({'name':k, 'value':v})
    exists = userPrefrences.objects.filter(user=request.user).exists()
    userprefrence = None

    if exists:
        userprefrence = userPrefrences.objects.get(user=request.user)
            #pdb.set_trace()
    if request.method == 'GET':
        return render(request, 'userprefrences/index.html', {'currencies':currency_data, 'user_preferences': userprefrence})

    else:
        currency = request.POST['currency']
        if exists:
            userprefrence.currency = currency
            userprefrence.save()

           
        else:
            userPrefrences.objects.create( user=request.user, currency=currency)
        messages.success(request, "Changes saved")
        return render(request, 'userprefrences/index.html', {'currencies':currency_data, 'user_preferences': userprefrence})
        