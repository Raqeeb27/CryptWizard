from datetime import datetime, timedelta
from decouple import config
from django.contrib import auth, messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse
from django.views.decorators.cache import cache_control, never_cache
from .encrypt_decrypt import *
import pyrebase


# Create your views here.
FIREBASE_CONFIG = {
    "apiKey": config('FIREBASE_API_KEY'),
    "authDomain": config('FIREBASE_AUTH_DOMAIN'),
    "databaseURL": config('FIREBASE_DATABASE_URL'),
    "projectId": config('FIREBASE_PROJECT_ID'),
    "storageBucket": config('FIREBASE_STORAGE_BUCKET'),
    "messagingSenderId": config('FIREBASE_MESSAGING_SENDER_ID'),
    "appId": config('FIREBASE_APP_ID'),
    "measurementId": config('FIREBASE_MEASUREMENT_ID')
}

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
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