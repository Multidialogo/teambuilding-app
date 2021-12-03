from django.urls import path
from events import views


urlpatterns = [
    path('', views.redirect_manage_own_events),
    path('create/', views.create_event, name='create_event'),
    path('manage/', views.manage_own_events, name='manage_own_events'),
    path('future/', views.future_events, name='future_events'),
    path('past/', views.past_events, name='past_events'),
]