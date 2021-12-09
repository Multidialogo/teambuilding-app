from django.urls import path

from products import views


urlpatterns = [
    path('add_producer/', views.redirect_add_producer_it, name='add_producer'),
    path('add_producer/<str:country>', views.add_producer, name='add_producer'),
]
