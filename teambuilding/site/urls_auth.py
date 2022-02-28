from django.urls import path

from . import views

urlpatterns = [
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('activate/<uidb64>/<token>/', views.activate_user, name='user-account-activate'),
    path('pass-reset/', views.password_reset, name="password-reset"),
    path('pass-reset/done/', views.PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('pass-reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'), # noqa
    path('pass-reset/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'), # noqa
]
