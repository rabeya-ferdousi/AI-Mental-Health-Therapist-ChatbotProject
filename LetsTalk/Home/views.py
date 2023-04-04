from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Client, Profile
from .forms import ClientForm


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
def profile(request, user_name):
    user = User.objects.get(username=user_name)
    client = Client.objects.get(user_ID=user.id)
    if (request.method == 'POST'):
        about_info = request.POST['about_info']
        if about_info != '':
            # to check if the profile already exists
            if Profile.objects.filter(client=client.id).exists():
                p = Profile.objects.get(client=client.id)
                p.about_info = about_info
                p.save()
            else:
                pro = Profile(about_info=about_info, client=client)
                pro.save()
    profile = Profile.objects.filter(client=client.id)
    if (profile.exists()):
        p = Profile.objects.get(client=client.id)
        name = str(client.first_name + " " + client.last_name).upper()
        birth_date = client.Date_Of_Birth
        about = p.about_info
        email = client.email
        gender = str(client.gender).upper()
    else:
        name = str(client.first_name + " " + client.last_name).upper()
        birth_date = client.Date_Of_Birth
        about = "USER HAS NOT ADDED ANY BIO OR PIC YET!!!!"  # hi i am oishi
        email = client.email
        gender = str(client.gender).upper()
    return render(request, 'Home/profile.html', {'user_name': user_name,
                                            'name': name,
                                            'bod': birth_date,'bio': about,
                                            'email': email,
                                            'gender': gender})

def password_reset(request, user_name):
    user = User.objects.get(username=user_name)
    username = user.first_name + ' ' + user.last_name
    if (request.method == 'POST'):
        password = request.POST['password']
        if user.password == password:
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']
            if new_password != '' and confirm_password != '':
                if new_password == confirm_password:
                    user.password = new_password
                    user.save()
                    client = Client.objects.get(user_ID=user.id)
                    client.password = new_password
                    client.save()
                    messages.success(request, 'Password updated.')
                    return redirect('profile', user_name=user_name)
                else:
                    messages.error(request, 'THE PASSWORDS DOES NOT MATCH !!!...')
            else:
                messages.error(request, 'Empty string not allowed as password!!!!')
        else:
            messages.error(request, 'WRONG USER PASSWORD ENTERED!!!!')

    return render(request, 'Home/update_password.html', {'user_name': username})

