from django.urls import path
from .views import auth_home, register_view, login_view, logout_view

urlpatterns = [
  path('', auth_home, name='auth_home'),
  path('register/', register_view, name='register'),
  path('login/', login_view, name='login'),
  path('logout/', logout_view, name='logout'),
]