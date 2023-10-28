from datetime import datetime, timedelta
from django.contrib import auth, messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from .encrypt_decrypt import *
import pyrebase


# Create your views here.
config = {
    "apiKey": "AIzaSyC35iHrX-arm-h-PQz1eFC3BjiH0d4pPfI",
    "authDomain": "cryptwizard-bf4b0.firebaseapp.com",
    "databaseURL": "https://cryptwizard-bf4b0-default-rtdb.firebaseio.com",
    "projectId": "cryptwizard-bf4b0",
    "storageBucket": "cryptwizard-bf4b0.appspot.com",
    "messagingSenderId": "881303371926",
    "appId": "1:881303371926:web:c703581b0754c05d1602b7",
    "measurementId": "G-46EH72X4MX"
}

firebase = pyrebase.initialize_app(config)
authorize = firebase.auth()
database = firebase.database()

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if confirm_password != password :
            messages.warning(request, "Passwords doesn't match! Registration Failed.", "warning")
            return redirect('register')
        
        try:
            user = authorize.create_user_with_email_and_password(email, password)

            uid = user['localId']
            encrypted_user_master_password = encrypt_password(uid,password)
            user_details = {'username':username, 'firstname':firstname, 'lastname':lastname, 'email':email, 'password':encrypted_user_master_password.decode('utf-8'), 'status':'1'}

            database.child("Users").child(uid).child('Details').set(user_details)

            session_id = user['idToken']
            request.session['user_session_id'] = str(session_id)
            
        except:
            messages.warning(request, "Email already exists! Registration Failed.", "warning")
            return redirect('register')

        messages.success(request, "Registeration Successfull!", "success")
        return redirect('dashboard')

    return render(request, 'register.html')

@never_cache
def signin(request):
    if request.session.get('user_session_id'):
        return redirect('dashboard')
    return render(request, 'signin.html')

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def dashboard(request):
    
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
        
            user = authorize.sign_in_with_email_and_password(email,password)
            session_id = user['idToken']
            user_session_id = str(session_id)
            request.session['user_session_id'] = user_session_id

            messages.success(request, "Logged in Successfully!", "success")
            return HttpResponseRedirect(reverse('dashboard'))
                   
        except:
            messages.warning(request, "Invalid Credentials!", "warning")
            return redirect('signin')
        
    elif not request.session.get('user_session_id'):
        messages.warning(request, "Session Expired! Please Sign in to access Dashboard.", "warning")
        return redirect('signin')
    
    else:
        user_session_id = request.session['user_session_id']

    a = authorize.get_account_info(user_session_id)
    a = a['users']
    a = a[0]
    user_localId = a['localId']
    name = database.child("Users").child(user_localId).child('Details').child('username').get().val()

    response = HttpResponse(render(request, 'dashboard.html', {'username': name}))

    expiration_date = datetime.now() + timedelta(minutes=30)
    response['Expires'] = expiration_date.strftime('%a, %d %b %Y %H:%M:%S GMT')

    return response

@never_cache
def logout(request):
    del request.session['user_session_id']
    auth.logout(request)
    messages.success(request, "Logged out Successfully!", "success")
    return HttpResponseRedirect(reverse('signin'))