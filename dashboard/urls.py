from django.urls import path
from django.views.generic import TemplateView

from .views import home_view, index, login_view, logout_view, boards_view, columns_view, index_col

urlpatterns = [
    path('home', home_view, name='home'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('boards', boards_view, name='boards'),
    path('columns/<int:board_id>/', columns_view, name='columns'),
    path('index_col', index_col, name='index_col'),
    path('register', TemplateView.as_view(template_name='dashboard/register.html')),
    path('new', TemplateView.as_view(template_name='dashboard/create_team.html')),

    path('',  index),
]