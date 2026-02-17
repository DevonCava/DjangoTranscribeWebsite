from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.users,),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logoutUser/', views.logoutUser, name='logoutUser'),
]