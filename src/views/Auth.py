from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.urls import reverse, reverse_lazy, resolve
from django.contrib.auth.decorators import login_required
from django.urls.resolvers import LocalePrefixPattern

# Create your views here.
def signin(request):

    username = password = ''

    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard')
    else:
        if request.POST:
            email=request.POST['username']
            password=request.POST['password']

            user= authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/dashboard')
                else:
                    messages.add_message(request, 'Akun anda belum diverifikasi pusat')
            else:
                messages.add_message(request, messages.INFO, 'Username atau password salah')

        return render(request, 'frontend/auth.html')

@login_required
def signout(request):
    logout(request)
    return redirect(reverse('core:dashboard'))