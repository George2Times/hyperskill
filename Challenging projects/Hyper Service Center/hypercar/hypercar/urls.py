"""hypercar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path
from django.views.generic import RedirectView
import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from tickets import views

urlpatterns = [
    path('welcome/', views.WelcomeView.as_view()),
    path('', views.MenuView.as_view()),
    path('menu/', views.MenuView.as_view()),
    re_path('get_ticket/(?P<service>[^/]*)/?', views.TicketView.as_view()),
    path('processing', views.ProcessingView.as_view()),
    path('processing/', RedirectView.as_view(url='/processing')),
    path('next/', views.NextClientView.as_view())
]