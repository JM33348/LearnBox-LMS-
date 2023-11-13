from email.message import EmailMessage
from Tools.scripts import generate_token
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
# from jwt.utils import force_bytes

from .forms import RegistrationForm, AccountAuthenticationForm
from verify_email.email_handler import send_verification_email

def activateEmail(request, user, email):
    mail_subject = 'Activate your LearnBox account'
    message = render_to_string('Accounts/activate.html', {
        'user': user,
        'domain': '127.0.0.1:8000',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user),
    })
    to_email = email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

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
            # print(form.cleaned_data['email'])
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
