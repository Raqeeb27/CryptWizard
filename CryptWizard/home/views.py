from django.shortcuts import redirect, render, HttpResponse
from django.contrib import auth, messages
import pyrebase
from .encrypt_decrypt import *


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

        try:
            user = auth.get_account_info(email)
            messages.error(request, "Email already exists! Registration Failed.")
            return redirect('register')
        except:
            pass

        if confirm_password != password :
            messages.error(request, "Passwords doesn't match! Registration Failed.")
            return redirect('register')
        
        try:
            user = authorize.create_user_with_email_and_password(email, password)
            uid = user['localId']
            encrypted_user_master_password = encrypt_password(uid,password)
            user_details = {'username':username, 'firstname':firstname, 'lastname':lastname, 'email':email, 'password':encrypted_user_master_password.decode('utf-8'), 'status':'1'}

            database.child("Users").child(uid).child('Details').set(user_details)
            
        except:
            messages.error(request, "Unable to Register user! Please enter valid Email and Password.")
            return redirect('register')

        messages.success(request, "Registeration Successfull!")
        return redirect('signin')

    return render(request, 'register.html')

def signin(request):
    return render(request, 'signin.html')

def dashboard(request):
    
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
        
            user = authorize.sign_in_with_email_and_password(email,password)
            session_id = user['idToken']
            a = authorize.get_account_info(session_id)
            a = a['users']
            a = a[0]
            user_localId = a['localId']
            name = database.child("Users").child(user_localId).child('Details').child('username').get().val()
            request.session['user_session_id'] = str(session_id)

            if not request.session.get('logged_in_successfully_message', False):
                messages.success(request, "Logged in Successfully!")
                request.session['logged_in_successfully_message'] = True        
        except:
            messages.error(request, "Invalid Credentials!")
            return redirect('signin')
        
    elif not request.session.get('user_session_id'):
        messages.error(request, "Session Expired! Please Sign in to access Dashboard.")
        return redirect('signin')
    
    else:
        user_session_id = request.session['user_session_id']
        a = authorize.get_account_info(user_session_id)
        a = a['users']
        a = a[0]
        user_localId = a['localId']
        name = database.child("Users").child(user_localId).child('Details').child('username').get().val()

    return render(request, 'dashboard.html', {'username': name})

def logout(request):
    auth.logout(request)
    request.session['logged_in_successfully_message'] = False
    messages.success(request, "Logged out Successfully!")
    return redirect('signin')