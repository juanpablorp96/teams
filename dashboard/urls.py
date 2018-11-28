from django.urls import path
from django.views.generic import TemplateView

from .views import home_view, index, login_view, logout_view, boards_view, columns_view, index_col, tasks_view
from .views import create_user_view, edit_column_view, edit_task_view, edit_board_view, delete_task_view
from .views import delete_column_view, delete_board_view
from team.views import team_manager_view

urlpatterns = [
    path('home', home_view, name='home'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('boards', boards_view, name='boards'),
    path('board=<int:board_id>', columns_view, name='columns'),
    path('column=<int:column_id>', tasks_view, name='tasks'),
    path('index_col', index_col, name='index_col'),
    path('register', create_user_view, name='create_user'),
    path('modal', TemplateView.as_view(template_name='dashboard/modal.html')),
    path('edit_board=<int:board_id>', edit_board_view, name='edit_board'),
    path('edit_column=<int:column_id>', edit_column_view, name='edit_column'),
    path('edit_task=<int:task_id>', edit_task_view, name='edit_task'),
    path('delete_task=<int:task_id>', delete_task_view, name='delete_task'),
    path('delete_column=<int:column_id>', delete_column_view, name='delete_column'),
    path('delete_board=<int:board_id>', delete_board_view, name='delete_board'),
    path('team_manager', team_manager_view, name='team_manager'),

    path('',  index),
]
