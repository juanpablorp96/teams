from datetime import datetime
from django.shortcuts import HttpResponse, render, Http404, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Board, Column


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
        slug = "{}-{}".format(name.lower().replace(' ','-'), datetime.today())

        # ACA ESTA EL PROBLEMA
        new_column = Column.objects.create(board= boards.index(), name=name, slug=slug)
        order_by = request.GET.get('order_by', 'create_date')
        search = request.GET.get('search', '')
        columns = Column.objects.order_by('{}'.format(order_by))
        context = {'columns': columns}
        return render(request, 'dashboard/index_col.html', context)
    else:
        return Http404('Not allowed')


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
        context = {'boards': boards}
        return render(request, 'dashboard/dashboard.html', context)
    elif request.method == 'POST':
        name = request.POST.get('name', None)
        slug = "{}-{}".format(name.lower().replace(' ','-'), datetime.today())
        new_board = Board.objects.create(name=name, slug=slug)
        order_by = request.GET.get('order_by', 'create_date')
        search = request.GET.get('search', '')
        boards = Board.objects.order_by('{}'.format(order_by))
        context = {'boards': boards}
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
        slug = "{}-{}".format(name.lower().replace(' ','-'), datetime.today())
        new_column = Column.objects.create(board=board, name=name, slug=slug)
        order_by = request.GET.get('order_by', 'create_date')
        search = request.GET.get('search', '')
        columns = Column.objects.order_by('{}'.format(order_by))
        context = {'columns': columns, 'board': board}
        return render(request, 'dashboard/board_columns.html', context)
    else:
        return Http404('Not allowed')