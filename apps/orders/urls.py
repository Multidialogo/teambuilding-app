from django.urls import path

from . import views

urlpatterns = [
    path('list_orders/<int:producer_id>', views.list_orders, name='list_orders'),
    path('<int:product_id>', views.purchase, name='purchase'),
    path('success/', views.purchase_success, name='purchase_success'),
    path('add_producer_order/<int:producer>', views.order_producer_create, name='add_producer_order'),

]
