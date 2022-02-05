from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.profile_detail, name='user-profile'),
    path('<int:pk>/profile/', views.profile_detail, name='user-profile'),
    path('profile/edit', views.profile_update, name='user-profile-update'),
    path('<int:pk>/profile/edit', views.profile_update, name='user-profile-update'),
    path('<int:pk>/happy_birthday', views.happy_birthday_send, name='user-happy-bday'),
    path('notifications/', views.notification_list, name='notification-list'),
    path('<int:user_pk>/notifications/', views.notification_list, name='notification-list'),
    path('notifications/<int:pk>', views.notification_detail, name='notification-detail'),
    path('<int:user_pk>/notifications/<int:pk>', views.notification_detail, name='notification-detail'), # noqa
]
