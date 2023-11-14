from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import RegistrationForm, AccountAuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from verify_email.email_handler import send_verification_email

User = get_user_model()

def verify_email(request, token):
    try:
        # Assuming you have a User model with an 'email_verification_token' field
        user = User.objects.get(email_verification_token=token, is_active=False)
        user.is_active = True
        user.email_verification_token = None  # You may want to clear the token after verification
        user.save()

        messages.success(request, 'Your email has been verified. You can now log in.')
        return redirect('login')

    except User.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('login')

def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}.")
    context = {}

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_verification_email(request, form)
            return redirect('home')
        else:
            context['registration_form'] = form

    return render(request, 'Accounts/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    destination = get_redirect_if_exists(request)
    print("destination: " + str(destination))

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                if destination:
                    return redirect(destination)
                return redirect("home")
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, "Accounts/login.html", context)

def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect
