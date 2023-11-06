from datetime import datetime, timedelta
from decouple import config
from django.contrib import auth, messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse
from django.views.decorators.cache import cache_control, never_cache
from .encrypt_decrypt import *
from .password_generator import password_gen
import pyrebase
from random import choice

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

dashboard_greetings = [
    "Bid farewell to password chaos! Discover the magic of effortless password management with CryptWizard right here on your dashboard.",
    "Say goodbye to password chaos and embrace the ease of password management with CryptWizard right on your dashboard.",
    "Escape the hassle of password chaos - experience seamless password management with CryptWizard, waiting for you here on your dashboard.",
    "It's time to wave goodbye to password chaos! Explore the simplicity of password management with CryptWizard directly on your dashboard.",
    "Break free from password chaos and unlock the convenience of effortless password management with CryptWizard, available right here on your dashboard.",
    "Say farewell to the chaos of passwords! Dive into the convenience of effortless password management with CryptWizard waiting for you on your dashboard.",
    "Say goodbye to password stress! Explore the enchanting world of effortless password management with CryptWizard here on your dashboard.",
    "Escape the maze of passwords and unlock the magic of easy password management with CryptWizard, available for you right on your dashboard.",
    "Say farewell to the hassle of passwords! Discover the ease of effortless password management with CryptWizard on your dashboard.",
    "Bid goodbye to password chaos and experience the simplicity of password management with CryptWizard, waiting for you on your dashboard."
]

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
            user_details = {
                'username':username, 
                'firstname':firstname, 
                'lastname':lastname, 
                'email':email, 
                'password':encrypted_user_master_password.decode('utf-8'), 
                'status':'1'
            }

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
    user_email = database.child("Users").child(user_localId).child('Details').child('email').get().val()
    first_name = database.child("Users").child(user_localId).child('Details').child('firstname').get().val()
    last_name = database.child("Users").child(user_localId).child('Details').child('lastname').get().val()

    set_status = "1"
    status_node_path = f"Users/{user_localId}/Details/status"
    database.child(status_node_path).set(set_status)

    content = {
        'username': name,
        'useremail':user_email,
        'firstname':first_name,
        'lastname':last_name,
        'randomDashboardGreeting': choice(dashboard_greetings),
    }

    response = HttpResponse(render(request, 'dashboard.html', content))

    expiration_date = datetime.now() + timedelta(minutes=30)
    response['Expires'] = expiration_date.strftime('%a, %d %b %Y %H:%M:%S GMT')

    return response

@never_cache
def logout(request):
    if request.session.get('user_session_id'):
        user_session_id = request.session['user_session_id']
        a = authorize.get_account_info(user_session_id)
        a = a['users']
        a = a[0]
        user_localId = a['localId']

        set_status = "0"
        status_node_path = f"Users/{user_localId}/Details/status"
        database.child(status_node_path).set(set_status)

        del request.session['user_session_id']
        auth.logout(request)
    messages.success(request, "Logged out Successfully!", "success")
    return HttpResponseRedirect(reverse('signin'))

def generate_password(request):
    generated_password = password_gen(15)
    return JsonResponse({'password': generated_password})