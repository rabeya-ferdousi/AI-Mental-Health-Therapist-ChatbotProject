from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Client, Profile, ChatBot_Message_Thread, ChatBot_Message
from .forms import ClientForm
import re

# Create your views here.

def loadpage(request):
    return render(request,'Home/loadpage.html',{})
def signup(request):

   if(request.method == 'POST'):
       form = ClientForm(request.POST)
       if form.is_valid():
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        email = request.POST['email']
        name = first_name+email
        if User.objects.filter(username=name).exists():
            messages.error(request, 'The person with this email is already a member...')
        else:
            user = User(password=password, username=name, last_name=last_name, email=email, first_name=first_name)
            user.save()
            user_again = User.objects.all()
            get_user = user_again.get(email=email)
            gender = request.POST['gender']
            birth_date = request.POST['Date_Of_Birth']
            client = Client(first_name=first_name, last_name=last_name, email=email, gender=gender, password=password, Date_Of_Birth=birth_date, user_ID=get_user)
            client.save()
            return redirect('login')
   form = ClientForm()
   context = {'User_form': form, }

   return render(request, 'Home/signup.html', context)

# Create your views here.
def login(request):
    if (request.method == 'POST'):
        client_email = request.POST['email']
        client_password = request.POST['password']
        if User.objects.filter(email=client_email).exists():
            users = User.objects.filter(email=client_email)
            for user in users:
                if user.password == client_password:
                    messages.success(request, 'Sucessfully Logged In.')
                    return redirect('homepage', user_name=user.username)
                else:
                    messages.error(request, 'Incorrect Password !! ')
        else:
            messages.error(request, 'Username does not exist. ')
    return render(request, 'Home/login.html')

def home_screen(request, user_name):
    return render(request, 'Home/home.html', {'user_name': user_name,})


