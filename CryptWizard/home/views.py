from django.shortcuts import redirect, render, HttpResponse
from django.contrib import auth, messages
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
            messages.error(request, "Passwords doesn't match! Registration Failed.")
            return redirect('register')
        
        try:
            user = authorize.create_user_with_email_and_password(email, password)
            uid = user['localId']
            user_details = {'username':username, 'firstname':firstname, 'lastname':lastname, 'email':email, 'password':password, 'status':'1'}

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
            request.session['user_session_id'] = str(session_id)

            if not request.session.get('logged_in_successfully_message', False):
                messages.success(request, "Logged in Successfully!")
                request.session['logged_in_successfully_message'] = True
            return render(request, 'dashboard.html',{'e':email})
        
        except:
            messages.error(request, "Invalid Credentials!")
            return redirect('signin')
    else:
        messages.error(request, "Please Sign in to access Dashboard.")
        return redirect('signin')

def logout(request):
    auth.logout(request)
    messages.success(request, "Logged out Successfully!")
    return redirect('signin')