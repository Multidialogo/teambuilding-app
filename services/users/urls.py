from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/signup/', views.signup, name='signup'),
    path('auth/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/change_nickname', views.change_nickname, name='change_nickname'),
    path('auth/activate/<uidb64>/<token>/', views.activate, name='activate'),
]
