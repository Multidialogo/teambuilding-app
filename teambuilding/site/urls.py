from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.profile_detail, name='user-profile'),
    path('profile/edit', views.profile_update, name='user-profile-update'),
    path('profile/<int:bday_user_pk>/wish_happy_birthday', views.happy_birthday_send, name='user-profile-happy-bday'),
    path('notifications/', views.notification_list, name='notification-list'),
    path('notifications/<int:pk>', views.notification_detail, name='notification-detail')
]
