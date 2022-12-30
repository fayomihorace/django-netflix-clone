"""django_netflix_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings            # Add this line
from django.conf.urls.static import static  # Add this line

from netflix.views import index_view # Add this line
from netflix.views import register_view # Add this line
from netflix.views import login_view # Add this line
from netflix.views import logout_view # Add this line
from netflix.views import watch_movie_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='home'), # Add this line
    path('watch', watch_movie_view, name='watch_movie'), # Add this line
    path('register', register_view, name='register'), # Add this line
    path('login', login_view, name='login'), # Add this line
    path('logout', logout_view, name='logout'), # Add this line
]
# Add the lines below
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
