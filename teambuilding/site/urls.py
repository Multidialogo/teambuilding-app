from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('profile/', views.profile_detail, name='user-profile'),
    path('profile/edit', views.profile_update, name='user-profile-update'),
    path('profile/<int:bday_user_pk>/wish_happy_birthday', views.happy_birthday_send, name='user-profile-happy-bday'),
    path('notifications/', views.notification_list, name='notification-list'),
    path('notifications/<int:pk>', views.notification_detail, name='notification-detail'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/signup/', views.signup, name='signup'),
    path('auth/login/', auth_views.LoginView.as_view(template_name='teambuilding/site/auth/login.html'),
         name='login'),
    path('auth/activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('auth/password-reset/', views.password_reset, name="password-reset"),
    path('auth/password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='teambuilding/site/auth/password_reset_done.html'),
         name='password-reset-done'),
    path('auth/password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="teambuilding/site/auth/password_reset_confirm.html"),
         name='password-reset-confirm'),
    path('auth/password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='teambuilding/site/auth/password_reset_complete.html'),
         name='password_reset_complete'),
]
