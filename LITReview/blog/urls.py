from django.urls import path
from . import views

urlpatterns = [
    # path('', views.review_list, name='review_list'),
    path('review/<id>/', views.review_detail, name='review_detail'),
    path('ticket/<id>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/<id>/respond/', views.ticket_respond, name='ticket_respond'),
    path('', views.ReviewListView.as_view(), name='review_list'),
    path('create_review/', views.review_create, name='review_create'),
    path('create_ticket/', views.ticket_create, name='ticket_create'),
]