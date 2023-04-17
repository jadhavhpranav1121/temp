from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.models import *


# Create your views here.
def admin_login(request):
    try:
        if request.user.is_authenticate:
            return redirect("/dashboard/")
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

            user_obj = authenticate(username=username, password=password)

            if user_obj and user_obj.is_superuser:
                login(request, user_obj)
                return redirect("/dashboard/")
            return redirect("/")
        return render(request, "login.html")
    except Exception as e:
        print(e)


def dashboard(request):
    return render(request, "dashboard.html")


def convict(request):
    objs = convict.objects.all()
    return render(request, "convict.html", {"objs": objs})


def Block(request):
    objs = Block.objects.all()
    return render(request, "convict.html", {"objs": objs})
