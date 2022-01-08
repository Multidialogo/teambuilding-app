from django.urls import path
from django.contrib.auth import views as auth_views

from apps.accounts import views
from apps.accounts.forms import LoginForm

urlpatterns = [
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', form_class=LoginForm), name='login'),
    path('activate/<uid_64>/<token>/', views.activate, name='activate'),
]
