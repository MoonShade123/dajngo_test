from django.urls import re_path, path
from .views import index, redirect_original, shorting_url, register, login, logout


app_name = 'shortener'

urlpatterns = [
    # re_path('', index, name='home'),
    re_path('index', index, name='home'),
    path('redirect_original/<slug:shorted_url>/', redirect_original, name='redirectoriginal'),
    re_path('shorting_url', shorting_url, name='shorting_url'),
    re_path('register', register, name='register'),
    re_path('login', login, name='login'),
    re_path('logout', logout, name='logout'),
]