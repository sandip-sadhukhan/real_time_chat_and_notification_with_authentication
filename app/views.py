from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.urls import reverse


def signup(request):
    # if authenticated then redirect to user
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home"))
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # create user
            User.objects.create_user(username, email, password)
        except Exception as e:
            messages.add_message(request, messages.ERROR, e)
            return HttpResponseRedirect(reverse("signup"))

        # authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.add_message(
                request, messages.SUCCESS, "Account Successfully Created!"
            )
            return HttpResponseRedirect(reverse("userHome"))
        else:
            messages.add_message(request, messages.ERROR, "Error ocurred")
            return HttpResponseRedirect(reverse("signup"))
    else:
        return render(request, "user/signup.html")


def login(request):
    # if authenticated then redirect to user
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home"))

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # authenticate
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.add_message(request, messages.SUCCESS, "You are LoggedIn")
            return HttpResponseRedirect(reverse("home"))
        else:
            messages.add_message(
                request, messages.ERROR, "Username or password not correct"
            )
            return HttpResponseRedirect(reverse("login"))
    else:
        return render(request, "user/login.html")


def logout(request):
    auth_logout(request)
    messages.add_message(request, messages.SUCCESS, "You are successfully logout.")
    return HttpResponseRedirect(reverse("login"))


@login_required
def home(request):
    # check superuser or not, then redirect to it's specific url
    user = request.user
    if user.is_superuser:
        return HttpResponseRedirect(reverse("adminHome"))
    else:
        return HttpResponseRedirect(reverse("userHome"))


@login_required
def adminHome(request):
    user = request.user
    # if the user is not superuser then redirect
    if not user.is_superuser:
        messages.add_message(
            request, messages.ERROR, "You are not authorized to view that page!"
        )
        return HttpResponseRedirect(reverse("userHome"))

    allUsers = User.objects.filter(is_superuser=False)
    context = {"allUsers": allUsers, "user": user}

    return render(request, "admin/all-users.html", context)


@login_required
def userHome(request):
    user = request.user
    # if the user is superuser then redirect
    if user.is_superuser:
        messages.add_message(
            request, messages.ERROR, "You are not authorized to view that page!"
        )
        return HttpResponseRedirect(reverse("adminHome"))

    context = {"user": user}

    return render(request, "user/user.html", context)


@login_required
def adminChat(request, userId):
    user = request.user
    # if the user is not superuser then redirect
    if not user.is_superuser:
        messages.add_message(
            request, messages.ERROR, "You are not authorized to view that page!"
        )
        return HttpResponseRedirect(reverse("userHome"))

    try:
        client = User.objects.get(id=userId)
    except User.DoesNotExist:
        messages.add_message(request, messages.ERROR, "User is not Found!")
        return HttpResponseRedirect(reverse("adminHome"))

    context = {"client": client, "user": user}

    return render(request, "admin/user-chat.html", context)
