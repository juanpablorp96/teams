from datetime import datetime
from django.shortcuts import render, Http404, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Board, Column, Task
from team.models import Team


def index(request):
    if request.method == 'GET':
        order_by = request.GET.get('order_by', 'create_date')
        search = request.GET.get('search', '')
        boards = Board.objects.order_by('{}'.format(order_by))
        context = {'boards': boards}
        return render(request, 'dashboard/index.html', context)
    elif request.method == 'POST':
        name = request.POST.get('name', None)
        slug = "{}-{}".format(name.lower().replace(' ','-'), datetime.today())
        new_board = Board.objects.create(name=name, slug=slug)
        context = {'message': 'Created!'}
        return render(request, 'dashboard/index.html', context)
    else:
        return Http404('Not allowed')


def index_col(request):
    if request.method == 'GET':
        order_by = request.GET.get('order_by', 'create_date')
        search = request.GET.get('search', '')
        columns = Column.objects.order_by('{}'.format(order_by))
        context = {'columns': columns}
        return render(request, 'dashboard/index_col.html', context)
    elif request.method == 'POST':
        name = request.POST.get('name', None)
        slug = "{}-{}".format(name.lower().replace(' ', '-'), datetime.today())

        # ACA ESTA EL PROBLEMA
        new_column = Column.objects.create(board= boards.index(), name=name, slug=slug)
        order_by = request.GET.get('order_by', 'create_date')
        search = request.GET.get('search', '')
        columns = Column.objects.order_by('{}'.format(order_by))
        context = {'columns': columns}
        return render(request, 'dashboard/index_col.html', context)
    else:
        return Http404('Not allowed')


def create_user_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        passw = request.POST.get("passw")
        user = User.objects.create_user(username, email, passw)
        return redirect('login')
    else:
        pass
    return render(request, 'dashboard/register.html')


def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get("username")
        passw = request.POST.get("passw")
        user = authenticate(request, username=username, password=passw)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            pass
    return render(request, 'dashboard/login.html', context)


def home_view(request):
    context = {"user": request.user}
    return render(request, 'dashboard/home.html', context)


def logout_view(request):
    logout(request)
    context = {"user": request.user}
    return render(request, 'dashboard/logout.html', context)


def boards_view(request):
    if request.method == 'GET':
        order_by = request.GET.get('order_by', 'create_date')
        search = request.GET.get('search', '')
        boards = Board.objects.order_by('{}'.format(order_by))
        teams = Team.objects.all()
        context = {'boards': boards, 'teams': teams}
        return render(request, 'dashboard/dashboard.html', context)
    elif request.method == 'POST':
        name = request.POST.get('name', None)
        team_id = request.POST.get('selected_team', None)
        team_associated = get_object_or_404(Team, pk=team_id)
        slug = "{}-{}".format(name.lower().replace(' ', '-'), datetime.today())
        new_board = Board.objects.create(name=name, slug=slug, team=team_associated)
        order_by = request.GET.get('order_by', 'create_date')
        search = request.GET.get('search', '')
        boards = Board.objects.order_by('{}'.format(order_by))
        teams = Team.objects.all()
        context = {'boards': boards, 'teams': teams}
        return render(request, 'dashboard/dashboard.html', context)
    else:
        return Http404('Not allowed')


def columns_view(request, board_id):
    board = get_object_or_404(Board, pk=board_id)

    if request.method == 'GET':
        order_by = request.GET.get('order_by', 'create_date')
        search = request.GET.get('search', '')
        columns = Column.objects.order_by('{}'.format(order_by))
        context = {'columns': columns, 'board': board}
        return render(request, 'dashboard/board_columns.html', context)
    elif request.method == 'POST':
        name = request.POST.get('name', None)
        slug = "{}-{}".format(name.lower().replace(' ', '-'), datetime.today())
        new_column = Column.objects.create(board=board, name=name, slug=slug)
        order_by = request.GET.get('order_by', 'create_date')
        search = request.GET.get('search', '')
        columns = Column.objects.order_by('{}'.format(order_by))
        context = {'columns': columns, 'board': board}
        return render(request, 'dashboard/board_columns.html', context)
    else:
        return Http404('Not allowed')


def tasks_view(request, column_id):
    column = get_object_or_404(Column, pk=column_id)
    users = User.objects.all()
    if request.method == 'GET':
        order_by = request.GET.get('order_by', 'create_date')
        search = request.GET.get('search', '')
        tasks = Task.objects.order_by('{}'.format(order_by))
        context = {'tasks': tasks, 'column': column, 'users': users}
        return render(request, 'dashboard/column_tasks.html', context)
    elif request.method == 'POST':
        title = request.POST.get('title', None)
        description = request.POST.get('description', None)
        user_id = request.POST.get('selected_user')
        in_charge = get_object_or_404(User, pk=user_id)
        new_task = Task.objects.create(column=column, title=title, description=description, in_charge=in_charge)
        order_by = request.GET.get('order_by', 'create_date')
        search = request.GET.get('search', '')
        tasks = Task.objects.order_by('{}'.format(order_by))
        context = {'tasks': tasks, 'column': column, 'users': users}
        return render(request, 'dashboard/column_tasks.html', context)
    else:
        return Http404('Not allowed')


# for edit functions they redirect to 'boards' view
# I try to redirect to the previous page but I can't because the params of the views
def edit_board_view(request, board_id):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('new_board_name', None)
        Board.objects.filter(pk=board_id).update(name=name)
        return redirect('boards')
    if request.method == 'GET':
        return render(request, 'dashboard/edit_board.html', context)

    else:
        return Http404('Not allowed')


def edit_column_view(request, column_id):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('new_column_name', None)
        Column.objects.filter(pk=column_id).update(name=name)
        return redirect('boards')
    if request.method == 'GET':
        return render(request, 'dashboard/edit_column.html', context)

    else:
        return Http404('Not allowed')


def edit_task_view(request, task_id):
    users = User.objects.all()
    context = {'users': users}
    if request.method == 'POST':
        title = request.POST.get('new_task_title', None)
        Task.objects.filter(pk=task_id).update(title=title)
        description = request.POST.get('new_task_description', None)
        Task.objects.filter(pk=task_id).update(description=description)
        user_id = request.POST.get('selected_user')
        in_charge = get_object_or_404(User, pk=user_id)
        Task.objects.filter(pk=task_id).update(in_charge=in_charge)
        return redirect('boards')
    if request.method == 'GET':
        return render(request, 'dashboard/edit_task.html', context)

    else:
        return Http404('Not allowed')

# DELETE !!!!!!!!!!!!!!!!!!!!!1


def delete_task_view(request, task_id):
    context = {}
    if request.method == 'POST':
        Task.objects.filter(pk=task_id).delete()
        return redirect('boards')
    if request.method == 'GET':
        return render(request, 'dashboard/delete_task.html', context)

    else:
        return Http404('Not allowed')


def delete_column_view(request, column_id):
    context = {}
    if request.method == 'POST':
        Column.objects.filter(pk=column_id).delete()
        return redirect('boards')
    if request.method == 'GET':
        return render(request, 'dashboard/delete_column.html', context)

    else:
        return Http404('Not allowed')


def delete_board_view(request, board_id):
    context = {}
    if request.method == 'POST':
        Board.objects.filter(pk=board_id).delete()
        return redirect('boards')
    if request.method == 'GET':
        return render(request, 'dashboard/delete_board.html', context)

    else:
        return Http404('Not allowed')
