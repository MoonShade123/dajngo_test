from sys import prefix
from django.shortcuts import render, get_object_or_404, redirect
import random, string, json
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth import authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .models import Url, User
from .forms import UserCreationForm, UserAuthenticateForm


@csrf_protect
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login_user(request, user)
            messages.success(request, "Registration successful." )
            return redirect("shortener:home")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserCreationForm()
    return render(request, "shortener/register.html", context={"register_form" : form})

@csrf_protect
def login(request):
    if request.method == "POST":
        form = UserAuthenticateForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login_user(request, user)
                messages.info(request, f"You are now logged in as {email}.")
                return redirect("shortener:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = UserAuthenticateForm()
    return render(request, "shortener/login.html", context={"login_form" : form})

def logout(request):
	logout_user(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("shortener:home")

@csrf_protect
def index(request):
    urls = Url.objects.all()
    try:
        previous_urls = Url.objects.filter(user=request.user)
    except:
        previous_urls = None
    prefix = settings.SITE_URL
    return render(request, 'shortener/index.html', context={'urls' : urls, 'prefix': prefix, 'previous_urls' : previous_urls})

def redirect_original(request, shorted_url):
    url = get_object_or_404(Url, shorted_url=shorted_url)
    return HttpResponseRedirect(url.default_url)

def shorting_url(request):
    url = request.POST.get("url", '')
    if not (url == ''):
        shorted_url = create_short_url()
        try:
            user = request.user
        except:
            user = None
        b = Url(default_url=url, shorted_url=shorted_url, user=user)
        b.save()
        response_data = {}
        response_data['url'] = settings.SITE_URL + "/" + shorted_url
        return HttpResponse(json.dumps(response_data),  content_type="application/json")
    return HttpResponse(json.dumps({"error": "error occurs"}), content_type="application/json")

def create_short_url():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    while True:
        shorted_url = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Url.objects.get(pk=shorted_url)
        except:
            return shorted_url
