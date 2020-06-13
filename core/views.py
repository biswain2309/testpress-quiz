from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

def signup(request):
    if request.method == 'POST':
        # User has info and wants an account now!
        if request.POST['Password1'] == request.POST['Password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'core/signup.html', {'error':'Username has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['Password1'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render(request, 'core/signup.html', {'error':'passwords must match'})
    else:
        # User wants to enter info
        return render(request, 'core/signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['Password'])
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request, 'core/login.html',{'error':'username or password is incorrect.'})
    else:
        return render(request, 'core/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')

