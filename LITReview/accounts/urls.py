from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register_view, name='register_view'),
    path('follows/', login_required(views.subscriptions), name='subscriptions'),
    path('unfollow/<id>', login_required(views.unfollow), name='unfollow'),
]