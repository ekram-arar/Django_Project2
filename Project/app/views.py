from django.shortcuts import render , redirect
from django.contrib import messages
import bcrypt
from .models import *

def about(request):
    return render(request, 'about.html')

def registration(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        email = request.POST['email']
        try:
            User.objects.get(email=email)
            messages.error(request, "A user with this email already exists")
            return redirect('/')
        except:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password = request.POST["password"]
            password = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
            this_user = User.objects.create(first_name = first_name,last_name = last_name, email = email, password = password)
            request.session['user_id'] = this_user.id
            errors["success"] = "Successfully registered (or logged in)!"
            return redirect('/')

def login(request):
    try:
        this_user = User.objects.get(email=request.POST['email'])
        if this_user:
            print(this_user.password)
            if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
                request.session['user_id'] = this_user.id
                messages.error(request, "Successfully registered (or logged in)!")
                return redirect('/')
            else:
                messages.error(request, "Wrong password")
                return redirect('/')
    except Exception as exp:
        messages.error(request, "Email not found: " + str(exp))
        return redirect('/')

def logout(request):
    del request.session['user_id']
    messages.error(request, "You have successfully logged out")
    return redirect('/')