
from django.shortcuts import render, redirect
from django.contrib import messages
from . models import *
from Admin.models import *

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']
        if password == confirm_password:
            if UserModel.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('register')
            else:
                user = UserModel.objects.create(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Registration Successfull!')
                return redirect('login')
        else:
            messages.error(request, 'Password and Confirm Password do not match')
            return redirect('register')
        
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email == 'admin@gmail.com' and password == 'admin':
            request.session['login']='admin'
            request.session['email']=email
            return redirect('home')
        elif UserModel.objects.filter(email=email,password=password).exists():
            request.session['login']='user'
            request.session['email']=email
            return redirect('home')
        else:
            messages.error(request, 'Invalid Email or Password')
            return redirect('login')
    return render(request, 'login.html')

def home(request):
    login = request.session['login']
    data = PapersModel.objects.all()
    return render(request, 'home.html',{'login':login,'data':data})


def logout(request):
    del request.session['login']
    del request.session['email']
    return redirect('index')


def viewpapers(request):
    login = request.session['login']
    print(login,"========================")
    data = PapersModel.objects.all()
    return render(request, 'viewpapers.html',{'login':login, 'data':data})


def searchpaper(request):
    login = request.session['login']
    if request.method == 'POST':
        search = request.POST['search']
        data = PapersModel.objects.filter(title__icontains=search)
        return render(request, 'viewpapers.html',{'login':login, 'data':data})
    





