from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.profile_detail, name='user-profile'),
    path('profile/edit', views.profile_update, name='user-profile-update'),
]
