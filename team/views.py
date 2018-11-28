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
        print("entre a POST")
        name = request.POST.get('name', None)
        print(name)
        user_id_list = request.POST.getlist('selected_users', None)
        users_list = []
        print(user_id_list)
        for user_id in user_id_list:
            users_list.append(get_object_or_404(User, pk=user_id))
        print(users_list)
        # print(member)
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

