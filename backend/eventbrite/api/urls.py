from django.urls import path
from functools import partial
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('fetch-all-events/', views.fetch_all_events, name='fetch_all_events'),
    path('getuser/<str:username>/', views.get_user_id_by_username, name='get_user_id_by_username'),
    path('create-event/<str:username>/', views.create_event_for_user, name='create_event_for_user'),
]