from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import RegistrationForm, AccountAuthenticationForm
from django.shortcuts import render, redirect
from verify_email.email_handler import send_verification_email

User = get_user_model()



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
