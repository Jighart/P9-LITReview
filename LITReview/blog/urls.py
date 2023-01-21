from django.urls import path
from . import views

urlpatterns = [
    # path('', views.review_list, name='review_list'),
    path('review/<id>/', views.review_detail, name='review_detail'),
    path('', views.ReviewListView.as_view(), name='review_list'),
    path('create/', views.review_create, name='review_create'),
]