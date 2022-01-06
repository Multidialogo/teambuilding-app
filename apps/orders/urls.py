from django.urls import path

from . import views

urlpatterns = [
    path('user/orders/', views.purchase, name='orders-user-purchase'),
    path('user/orders/<int:product_id>', views.purchase, name='orders-user-purchase'),
    path('staff/orders/list/', views.list_manage, name='orders-staff-list-manage'),
    path('staff/orders/list/<int:producer_id>', views.list_manage, name='orders-staff-list-manage'),
    path('staff/orders/send/<int:producer_id>', views.send_to_producer, name='orders-staff-send-to-producer'),
    path('staff/orders/send/<int:producer_id>/<str:country>', views.send_to_producer, name='orders-staff-send-to-producer'),
]
