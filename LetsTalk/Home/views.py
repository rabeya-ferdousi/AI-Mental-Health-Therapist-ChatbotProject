from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Client, Profile, ChatBot_Message_Thread, ChatBot_Message
from .forms import ClientForm
import openai
import re

# Create your views here.

def loadpage(request):
    return render(request,'Home/loadpage.html',{})


def dairy(request,user_name):

   return render(request,'Home/diary.html',{})


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
                                                 'bod': birth_date, 'bio': about,
                                                 'email': email,
                                                 'gender': gender})

def getMessagesRobo(request, user_id):
    list = []
    if ChatBot_Message_Thread.objects.filter(client=user_id).exists():
        chat = ChatBot_Message_Thread.objects.get(client=user_id)
        thread_Id = chat.id
        msgs = ChatBot_Message.objects.filter(Thread_Id=thread_Id)
        list = []
        for messages in msgs:
            userchat = messages.Client_Message
            reply = messages.Therapist_Message
            time = (messages.Message_Time).strftime("%m/%d/%Y, %H:%M:%S")
            sender = Client.objects.get(id=user_id)
            #sender_name = sender.f_name + " " + sender.l_name
            history1 = str('YOU  :' + userchat + ', TIME :' + time)
            list.append(history1)
            history2 = str('ROBO  :' + reply + '\n' + ', TIME :' + time)
            list.append(history2)
    return list
def chat_with_bot_page(request, user_name):
    user = User.objects.get(username=user_name)
    username = user.first_name + ' ' + user.last_name
    client = Client.objects.get(user_ID=user.id)
    client_id = client.id
    list = getMessagesRobo(request, user_id=client_id)
    prompt_list: list[str] = ['You are a Chatbot and will answer as a Chatbot',
                              '\nHuman: What time is it?',
                              '\nAI: I have no idea, I\'m a Chatbot!']
    if (request.method == 'POST'):
        message = request.POST['message']
        if message != '':
            if ChatBot_Message_Thread.objects.filter(client=client_id).exists():
                # get the messege from thread and save gessege
                thread = ChatBot_Message_Thread.objects.get(client=client_id)
                response: str = get_bot_response(message, prompt_list)
                new_msg = ChatBot_Message(Client_Message=message, Therapist_Message=response, Thread_Id=thread)
                new_msg.save()
                list = getMessagesRobo(request, user_id=client_id)


            else:
                # save msg and reply from robo for each msg
                therapist = ChatBot_Message_Thread(client=client)
                therapist.save()
                thread = ChatBot_Message_Thread.objects.get(client=client_id)
                response: str = get_bot_response(message, prompt_list)
                new_msg = ChatBot_Message(Client_Message=message, Therapist_Message=response, Thread_Id=thread)
                new_msg.save()
                list = getMessagesRobo(request, user_id=client_id)
        else:
            pass
    return render(request, 'Home/botchat.html', {'user_full_name': username.upper(),
                                            'user_name': user_name,
                                            'messages': list})


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

# def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
#     message_certainty = 0
#     has_required_words = True
#
#     # Counts how many words are present in each predefined message
#     for word in user_message:
#         if word in recognised_words:
#             message_certainty += 1
#
#     # Calculates the percent of recognised words in a user message
#     percentage = float(message_certainty) / float(len(recognised_words))
#
#     # Checks that the required words are in the string
#     for word in required_words:
#         if word not in user_message:
#             has_required_words = False
#             break
#
#     # Must either have the required words, or be a single response
#     if has_required_words or single_response:
#         return int(percentage * 100)
#     else:
#         return 0
# def check_all_messages(message):
#     highest_prob_list = {}
#
#     # Simplifies response creation / adds it to the dict
#     def response(bot_response, list_of_words, single_response=False, required_words=[]):
#         nonlocal highest_prob_list
#         highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)
#
#     # Responses -------------------------------------------------------------------------------------------------------
#     response('Hello!', ['hello', 'hi', 'hey', 'Yo'], single_response=True)
#     response('See you!', ['bye', 'goodbye'], single_response=True)
#     response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how', 'are', 'you'])
#     response('Perfectly fine', ['how', 'is', 'your', 'day'], required_words=['how', 'day'])
#     response('Robo', ['what', 'is', 'your', 'name'], required_words=['your', 'name'])
#     response('My pleasure..', ['thank you', 'thanks'], single_response=True)
#     response('You don\'t have to say that!!!Anyway,Thank you!', ['you', 'are', 'nice'], required_words=['you', 'nice'])
#     response('Thanks!', ['you', 'are', 'sweet'], required_words=['you', 'sweet'])
#     response('I am a bot my origin is processor!!!',['where','are','you','from'] , required_words=['where', 'you', 'from'])
#     response('I am as old as the website', ['how', 'old', 'are', 'you'], required_words=['how', 'old'])
#     response('My age is the same as the website', ['what', 'is', 'your', 'age'], required_words=['your', 'age'])
#     response('I do not have any particular favourite color, but I love BLACK', ['your', 'color'], required_words=['color','black'])
#     response('It is a good invention of you humans but for details use the search box please', ['Where','what', 'is', 'internet'], required_words=['internet'])
#     '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''
#     response('Great!!!', ['i', 'am', 'fine'], required_words=['fine'])
#     response('My pleasure..', ['thank you', 'thanks'], single_response=True)
#     response('You don\'t have to say that!!!Anyway,Thank you!', ['you', 'are', 'nice'], required_words=['you', 'nice'])
#     response('Thanks!', ['you', 'are', 'sweet'], required_words=['you', 'sweet'])
#     response('I am a bot my origin is processor!!!', ['where', 'are', 'you', 'from'],
#              required_words=['where', 'you', 'from'])
#     response('I am as old as the website', ['how', 'old', 'are', 'you'], required_words=['how', 'old'])
#     response('My age is the same as the website', ['what', 'is', 'your', 'age'], required_words=['your', 'age'])
#     response('I do not have any particular favourite color, but I love BLACK',
#              ['what', 'is', 'your', 'favourite', 'color'], required_words=['color', 'favourite'])
#     response('It is a good invention of you humans but for details use the search box please',
#              ['Where', 'what', 'is', 'internet'], required_words=['internet'])
#     response('AAAAhhhh!!! I do not watch TV that much!!!', ['what', 'is', 'your', 'favourite', 'show'],
#              required_words=['favourite', 'show'])
#     response('You are a human of course and you are a member of friends website!!! Haha!!', ['do', 'you', 'know', 'me'],
#              required_words=['you', 'know'])
#     response(
#         'Facebook is a social networking site that makes it easy for you to connect and share with family and friends online.For more information please got to the query box.',
#         ['what', 'is', 'facebook'], required_words=['what', 'facebook'])
#     response('Google is a search engine!!!For more information please go to the query box!!', ['what', 'is', 'google'],
#              required_words=['what', 'google'])
#     response('YouTube is a free video sharing website!! For more information, use query box', ['what', 'is', 'youtube'],
#              required_words=['what', 'youtube'])
#
#     def unknown():
#         response = ["Could you please re-write that on query-box? ",
#                     "Sorry!!I may help you from the query-box",
#                     "I can help you through the query-box",
#                     "please go to the query-box"][
#             random.randrange(4)]
#         return response
#
#     # Longer responses
#     R_EATING = "I don't like eating anything because I'm a bot obviously!"
#     response(R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])
#     response(R_EATING, ['what', 'is', 'your', 'food'], required_words=['food'])
#
#     best_match = max(highest_prob_list, key=highest_prob_list.get)
#
#     return unknown() if highest_prob_list[best_match] < 1 else best_match
#
#
# # Used to get the response
# def get_response(user_input):
#     split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
#     response = check_all_messages(split_message)
#     return response


with open('Home/hidden.txt') as file:
    openai.api_key = file.read()

def get_api_response(prompt: str) -> str | None:
    text: str | None = None

    try:
        response: dict = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=60,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0,
            stop=["You:"]
        )

        choices: dict = response.get('choices')[0]
        text = choices.get('text')

    except Exception as e:
        print('ERROR:', e)

    return text


def update_list(message: str, pl: list[str]):
    pl.append(message)


def create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt


def get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
        pos: int = bot_response.find('\nAI: ')
        bot_response = bot_response[pos + 5:]
    else:
        bot_response = 'Something went wrong...'

    return bot_response


