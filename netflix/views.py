from importlib import invalidate_caches
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout

from .forms import RegisterForm
from .forms import LoginForm
from .forms import SearchForm
from .models import Movie

PAGE_SIZE_PER_CATEGORY = 20


def index_view(request):
    """Home page view."""
    # We define the list of categories we want to display
    categories_to_display = ['Action', 'Adventure']

    data = {}
    # We create a dictionary that map each category with the it movies
    for category_name in categories_to_display:
        movies = Movie.objects.filter(category__name=category_name)
        if request.method == 'POST':
            search_text = request.POST.get('search_text')
            movies = movies.filter(name__icontains=search_text)
        # we limit the number of movies to PAGE_SIZE_PER_CATEGORY = 20
        data[category_name] = movies[:PAGE_SIZE_PER_CATEGORY]

    search_form = SearchForm()
    # We return the response with the data
    return render(request, 'netflix/index.html', {
        'data': data.items(),
        'search_form': search_form
    })


def watch_movie_view(request):
    """Watch view."""
    # The primary key of the movie the user want to watch is sent by GET parameters.
    # We retrieve that pk.
    movie_pk = request.GET.get('movie_pk')
    # We try to get from the database the movie with the given pk 
    try:
        movie = Movie.objects.get(pk=movie_pk)
    except Movie.DoesNotExist:
        # if that movie doesn't exist, Movie.DoesNotExist exception is raised
        # and we then catch it and set the url to None instead
        movie = None
    return render(request, 'netflix/watch_movie.html', {'movie': movie})


def register_view(request):
    """Registration view."""
    if request.method == 'GET':
        # executed to render the registration page
        register_form = RegisterForm()
        return render(request, 'netflix/register.html', locals())
    else:
        # executed on registration form submission
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            User.objects.create(
                first_name=request.POST.get('firstname'),
                last_name=request.POST.get('lastname'),
                email=request.POST.get('email'),
                username=request.POST.get('email'),
                password=make_password(request.POST.get('password'))
            )
            return HttpResponseRedirect('/login')
        return render(request, 'netflix/register.html', locals())


def login_view(request):
    """Login view."""
    if request.method == 'GET':
        # executed to render the login page
        login_form = LoginForm()
        return render(request, 'netflix/login.html', locals())
    else:
        # get user credentials input
        username = request.POST['email']
        password = request.POST['password']
        # If the email provided by user exists and match the
        # password he provided, then we authenticate him.
        user = authenticate(username=username, password=password)
        if user is not None:
            # if the credentials are good, we login the user
            login(request, user)
            # then we redirect him to home page
            return HttpResponseRedirect('/')
        # if the credentials are wrong, we redirect him to login and let him know
        return render(
            request,
            'netflix/login.html',
            {
                'wrong_credentials': True,
                'login_form': LoginForm(request.POST)
            }
        )

def logout_view(request):
    """Logout view."""
    # logout the request
    logout(request)
    # redirect user to home page
    return HttpResponseRedirect('/')
