from datetime import datetime
from django.shortcuts import render, Http404, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Team


def team_manager_view(request):
    users = User.objects.all()

    if request.method == 'GET':
        order_by = request.GET.get('order_by', 'create_date')
        search = request.GET.get('search', '')
        teams = Team.objects.order_by('{}'.format(order_by))
        context = {'teams': teams, 'users': users}
        return render(request, 'team/team_manager.html', context)
    elif request.method == 'POST':
        name = request.POST.get('name', None)
        user_id_list = request.POST.getlist('selected_users', None)
        users_list = []
        for user_id in user_id_list:
            users_list.append(get_object_or_404(User, pk=user_id))
        slug = "{}-{}".format(name.lower().replace(' ', '-'), datetime.today())
        new_team = Team.objects.create(name=name, slug=slug)
        new_team.members.set(users_list)
        order_by = request.GET.get('order_by', 'create_date')
        search = request.GET.get('search', '')
        teams = Team.objects.order_by('{}'.format(order_by))
        context = {'teams': teams, 'users': users}

        return render(request, 'team/team_manager.html', context)
    else:
        return Http404('Not allowed')


def edit_team_view(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    users = User.objects.all()
    context = {'users': users}
    if request.method == 'POST':
        name = request.POST.get('new_team_name', None)
        new_users_list = request.POST.getlist('new_selected_users', None)
        users_list = []
        for user_id in new_users_list:
            users_list.append(get_object_or_404(User, pk=user_id))
        Team.objects.filter(pk=team_id).update(name=name)
        team.members.set(users_list)
        return redirect('team_manager')
    if request.method == 'GET':
        return render(request, 'team/edit_team.html', context)

    else:
        return Http404('Not allowed')


def delete_team_view(request, team_id):
    context = {}
    if request.method == 'POST':
        Team.objects.filter(pk=team_id).delete()
        return redirect('team_manager')
    if request.method == 'GET':
        return render(request, 'team/delete_team.html', context)

    else:
        return Http404('Not allowed')
