from django.urls import path
from . import views

urlpatterns = [
    # Admin URLs
    path('admin/create/', views.create_poll, name='create_poll'),
    path('admin/results/', views.view_poll_results_admin, name='poll_results_admin'),
    path('admin/results/<int:pk>/', views.poll_detail_admin, name='poll_detail_admin'),

    # Student URLs
    path('', views.poll_list, name='poll_list'),
    path('<int:pk>/vote/', views.vote_in_poll, name='vote_in_poll'),
    path('<int:pk>/results/', views.poll_results, name='poll_results'),
]
