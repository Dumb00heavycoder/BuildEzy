from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('create/', views.create_project_view, name='create_project'),
    path('project/<int:project_id>/', views.project_detail_view, name='project_detail'),
]
