from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from accounts.forms import RegistrationForm, FollowForm
from .models import UserFollow


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Connecté !')
                return redirect('feed')
            else:
                messages.error(request, 'Echec de connexion, vérifiez vos identifiants')
                return redirect('login_view')
        else:
            return render(request, 'registration/login.html', {})
    else:
        return redirect('feed')


def logout_view(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté du compte')
    return redirect('login_view')


def register_view(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()

            messages.success(request, 'Votre compte a bien été créé !')
            return redirect('login_view')
        else:
            return render(request, 'registration/register.html', {'user_form': user_form})
    else:
        user_form = RegistrationForm()
        return render(request, 'registration/register.html', {'user_form': user_form})


def subscriptions(request):
    if request.method == 'POST':
        follow_form = FollowForm(request.POST)

        if follow_form.is_valid():
            try:
                followed_user = User.objects.get(username=request.POST['followed_user'])
                if request.user == followed_user:
                    messages.error(request, 'Vous ne pouvez pas vous suivre vous-même !')
                else:
                    try:
                        UserFollow.objects.create(user=request.user, followed_user=followed_user)
                        messages.success(request, f'Vous suivez désormais {followed_user}!')
                    except IntegrityError:
                        messages.error(request, f'Vous suivez déjà {followed_user}!')

            except User.DoesNotExist:
                messages.error(request, f'L\'utilistateur {follow_form.data["followed_user"]} n\'existe pas !')


    else:
        follow_form = FollowForm()

    user_follows = UserFollow.objects.filter(user=request.user).order_by('followed_user')
    followed_by = UserFollow.objects.filter(followed_user=request.user).order_by('user')

    context = {
        'follow_form': follow_form,
        'user_follows': user_follows,
        'followed_by': followed_by,
        'title': 'Abonnements',
    }
    return render(request, 'follows.html', context)


def unfollow(request, id):
    follow = get_object_or_404(UserFollow, id=id)

    if follow.user != request.user:
        raise PermissionDenied()

    if request.method == 'GET':
        follow.delete()
        messages.info(request, f'Vous ne suivez plus {follow.followed_user}!')
        return redirect('follows')

    return redirect('follows')