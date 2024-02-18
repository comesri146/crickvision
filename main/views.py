from django.shortcuts import render, redirect
from django.contrib import auth
import pyrebase
from django.contrib.auth import logout
import requests
import numpy as np
from django.shortcuts import render
from django.contrib import auth
import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID"),
}




firebase = pyrebase.initialize_app(config)
database = firebase.database()
authe = firebase.auth()
global local_id
global name

def showWelcomePage(request):
    print(request)
    return render(request, "index.html")

def showSignin(request):
    return render(request, "auth.html",{"page":"signin"})

def showSignup(request):
    return render(request, "auth.html",{"page":"signup"})

def showForgotPass(request):
    return render(request, "auth.html",{"page":"forgotpass"})

def validateForgotPass(request):
    if request.method == "POST":
        email = request.POST.get('emailf')
        sendem = authe.send_password_reset_email(email)
        print(sendem)
        message = "An password reset email has been sent to " + sendem.get('email') +", follow the steps there."
        return render(request,"auth.html",{"page":"signin","msg":message})
    
def signInValidate(request):
    global local_id
    global idtoken
    if request.method == "POST":
        email = request.POST.get("emailx")
        password = request.POST.get("passx")
        try:
            user = authe.sign_in_with_email_and_password(email, password)
            if user is not None and "idToken" in user:
                idtoken = user["idToken"]
                user_info = authe.get_account_info(idtoken)
                email_verified = user_info['users'][0]['emailVerified']
                if email_verified:
                    local_id = user_info["users"][0]["localId"]
                    name = database.child("users").child(local_id).child("details").child("name").get().val()
                    vcount = int(database.child("users").child(local_id).child("details").child("videos").get().val())
                    #newcount = int(vcount) + 1
                    #database.child("users").child(local_id).child("details").child("videos").set(newcount)
                    print(vcount)
                    if 10 < vcount:
                        fbdata = config
                        credit = 0
                        creditl = "NO CREDITS LEFT"
                        return render(request,"welcome.html", {"name":name, "fbdata": fbdata, "userid": local_id,"vcount":vcount,"credit": credit,"creditl":creditl, "block": 1})

                    else:
                        fbdata = config
                        print("inelse")
                        credit = 10 - vcount
                        if credit == 1:
                            creditl = "CREDIT LEFT"
                        else:
                            creditl = "CREDITS LEFT"
                        return render(request,"welcome.html", {"name":name, "fbdata": fbdata, "userid": local_id,"vcount":vcount,"credit": credit,"creditl":creditl, "block": 0})

                else:
                    message = "Email is not verified, kindly verify your Email before signing in!"
                    return render(request, "auth.html",{"page":"signin","msg":message})
            else:
                message = "User not found"
                return render(request, "auth.html", {"page":"signin","msg": message})
        except Exception as e:
            message = "Invalid credentials" + str(e)
            return render(request, "auth.html", {"page":"signin","msg": message})
    return render(request, "auth.html",{"page":"signin"})
    
def signUpValidate(request):
    global local_id
    name = request.POST.get("name")
    email = request.POST.get("email")
    passw = request.POST.get("pass")
    try:
        user = authe.create_user_with_email_and_password(email, passw)
        authe.send_email_verification(user["idToken"])
    except Exception as e:
        msg = "Unable to create account. Try again"
        return render(request, "auth.html", {"msg":msg,"page":"signin"})
    uid = user["localId"]
    local_id = uid
    data = {
        "name": name,
        "status": "1",
        "email": email,
        "videos": "0",
        
    }
    msg = "An verification Email has been sent to your email, Verify your email and proceed to login"
    database.child("users").child(uid).child("details").set(data)
    return render(request, "auth.html",{"msg":msg,"page":"signin"})

def logoutProcess(request):
    apl = auth.logout(request)
    print(apl)
    return render(request,"auth.html",{"page":"signin","msg":"Thank you, Visit again!"})

def uploadVideo(request):
    global idtoken
    if request.method == "POST":
        something = request.POST.get("videoFile")
        print(something)
    return render(request,"welcome.html")

def videoProcess(request):
    global local_id
    if request.method == "POST":
        vidUrl = request.POST.get("vidUrl")
        database.child("users").child(local_id).child("details").child("uploads").child().set(vidUrl)
        print(vidUrl)
        return render(request, "output.html",{"url":vidUrl})