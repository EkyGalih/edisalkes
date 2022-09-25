from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.urls import reverse, reverse_lazy, resolve
from django.contrib.auth.decorators import login_required

def landing(request):
    return render(request, 'frontend/landing.html')