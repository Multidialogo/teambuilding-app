from django.urls import path

from products import views


urlpatterns = [
    path('add_producer/', views.add_producer, name='add_producer'),
]
