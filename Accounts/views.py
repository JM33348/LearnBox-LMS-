from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import RegistrationForm, AccountAuthenticationForm, EditProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from verify_email.email_handler import send_verification_email
from Accounts.models import Account
from django.conf import settings
from django.contrib import messages


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


def profile_view(request, *args, **kwargs):
    context = {}
    user_id = kwargs.get("user_id")
    try:
        account = Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        return HttpResponse("Something went wrong.")
    if account:
        context['id'] = account.id
        context['firstname'] = account.firstname
        context['lastname'] = account.lastname
        context['email'] = account.email
        context['profile_image'] = account.profile_image.url
        context['is_owner'] = request.user == account

        # Define template variables
        is_self = True
        is_friend = False
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False

        # Set the template variables to the values
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL
        return render(request, "Accounts/profile.html", context)

def edit_profile(request, user_id):
    # Fetch the Account instance based on user_id
    account = get_object_or_404(Account, pk=user_id)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile', user_id=account.id)
    else:
        form = EditProfileForm(instance=account)

    return render(request, 'Accounts/edit_profile.html', {'form': form, 'account': account})