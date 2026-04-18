from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        # Validate passwords match
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/signup.html')

        # Validate username not taken
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Please choose another.')
            return render(request, 'accounts/signup.html')

        # Create user (stored permanently in the database)
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('login')

    return render(request, 'accounts/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Check if the user even exists in the database
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'User not found.')
            return render(request, 'accounts/login.html')

        # User exists — try to authenticate (wrong password case)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # will change this to dashboard later on
        else:
            messages.error(request, 'Incorrect password. Please try again.')
            return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
