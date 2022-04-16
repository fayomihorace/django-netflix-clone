from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .forms import RegisterForm


def index_view(request):
    """Home page view."""
    return render(request, 'netflix/index.html')

def register_view(request):
    """Registration view."""
    if request.method == 'GET':
        # executed to render the registration page
        register_form = RegisterForm()
        return render(request, 'netflix/register.html', locals())
    else:
        # executed on registration form submission
        form = RegisterForm(request.POST)
        if form.is_valid():
            '''User.objects.create(
                first_name=request.POST.get('firstname'),
                last_name=request.POST.get('lastname'),
                email=request.POST.get('email'),
                username=request.POST.get('email'),
                password=make_password(request.POST.get('password'))
            )'''
            return HttpResponseRedirect('/login')
        return HttpResponse(form.errors)