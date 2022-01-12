from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='teambuilding/account/login.html'), name='login'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('password-reset/', views.password_reset, name="password-reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='teambuilding/account/password_reset_done.html'), name='password-reset-done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="teambuilding/account/password_reset_confirm.html"), name='password-reset-confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='teambuilding/account/password_reset_complete.html'), name='password_reset_complete'),
]
