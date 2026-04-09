from django.urls import path 
from . import views 

urlpatterns = [ 
               path('', view.dashboard_view, name='dashboard'),
               ]
