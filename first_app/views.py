from django.shortcuts import render, redirect 
from .forms import RegisterForm, ChangeUserData
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm # here we found user name and password
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                messages.success(request, 'Account created successfully!')
                form.save()
        else:
            form = RegisterForm()
        return render(request, 'signup.html', {'form':form})
    else:
        return redirect('profile')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data = request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                userpass = form.cleaned_data['password']
                user = authenticate(username=username, password = userpass) # checking the user has been in database or not
                if user is not None:
                    login(request, user)
                    return redirect('profile') #after login it redirect to profile page
        
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})
    
    else:
        return redirect('profile')

def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangeUserData(request.POST, instance = request.user)
            if form.is_valid():
                messages.success(request, 'Account updated successfully!')
                form.save()
        else:
            form = ChangeUserData( instance = request.user)
        return render(request, 'profile.html', {'form':form})
    else:
        return redirect('signup ')

def user_logout(request):
    logout(request)
    return redirect('login')

def pass_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user) #password update korbe
                return redirect('profile')
        else:
            form = PasswordChangeForm(user=request.user)

        return render(request, 'passchange.html', {'form':form})
    else:
        return redirect('login')

def pass_change2(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SetPasswordForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user) #password update korbe
                return redirect('profile')
        else:
            form = SetPasswordForm(user=request.user)

        return render(request, 'passchange.html', {'form':form})
    else:
         return redirect('login')
    