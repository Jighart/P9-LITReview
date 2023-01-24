from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.feed), name='review_list'),
    path('create_review/', login_required(views.review_create), name='review_create'),
    path('create_ticket/', login_required(views.ticket_create), name='ticket_create'),
    path('review/<id>/', login_required(views.review_detail), name='review_detail'),
    path('review/<id>/edit/', login_required(views.review_edit), name='review_edit'),
    path('review/<id>/delete/', login_required(views.review_delete), name='review_delete'),
    path('ticket/<id>/', login_required(views.ticket_detail), name='ticket_detail'),
    path('ticket/<id>/respond/', login_required(views.ticket_respond), name='ticket_respond'),
    path('ticket/<id>/edit/', login_required(views.ticket_edit), name='ticket_edit'),
    path('ticket/<id>/delete/', login_required(views.ticket_delete), name='ticket_delete'),
]