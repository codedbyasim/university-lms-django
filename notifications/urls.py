from django.urls import path
from . import views

urlpatterns = [
    # Admin URL
    path('admin/create/', views.create_notification, name='create_notification'),

    # Common URL for all roles
    path('', views.notifications_list, name='notifications_list'),
]
