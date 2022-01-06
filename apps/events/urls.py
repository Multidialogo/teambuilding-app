from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='event-all-list-upcoming')),
    path('all/', RedirectView.as_view(pattern_name='event-all-list-upcoming')),
    path('all/<int:pk>/', views.detail, name='event-detail'),
    path('all/upcoming/', views.list_upcoming_by_all, name='event-all-list-upcoming'),
    path('all/history/', views.list_past_by_all, name='event-all-list-history'),
    path('user/', views.list_upcoming_by_self, name='event-user-list'),
    path('user/new/', views.create, name='event-create'),
    path('user/<int:pk>/edit/', views.update, name='event-update'),
    path('user/<int:pk>/delete/', views.delete, name='event-delete'),
]
