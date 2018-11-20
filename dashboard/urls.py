from django.urls import path
from django.views.generic import TemplateView

from .views import home, index, login_view, logout_view

urlpatterns = [
    path('home', home, name='home'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('boards', TemplateView.as_view(template_name='bootstrap/dashboard.html')),
    path('register', TemplateView.as_view(template_name='bootstrap/register.html')),
    path('new', TemplateView.as_view(template_name='bootstrap/create_team.html')),

    path('',  index),
]