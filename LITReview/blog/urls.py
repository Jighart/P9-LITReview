from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReviewListView.as_view(), name='review_list'),
    path('create_review/', views.review_create, name='review_create'),
    path('create_ticket/', views.ticket_create, name='ticket_create'),
    path('review/<id>/', views.review_detail, name='review_detail'),
    path('review/<id>/edit/', views.review_edit, name='review_edit'),
    path('review/<id>/delete/', views.review_delete, name='review_delete'),
    path('ticket/<id>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/<id>/respond/', views.ticket_respond, name='ticket_respond'),
    path('ticket/<id>/edit/', views.ticket_edit, name='ticket_edit'),
    path('ticket/<id>/delete/', views.ticket_delete, name='ticket_delete'),
]