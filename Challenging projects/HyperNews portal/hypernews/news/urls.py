from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('', views.coming_soon, name='coming_soon'),
    path('news/', views.Index.as_view()),
    path('news/<int:link>/', views.NewsView.as_view()),
    path('news/create/', views.CreateNewsView.as_view()),

    path('admin/', admin.site.urls),
]
