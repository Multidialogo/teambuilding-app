from django.urls import path

from products import views

urlpatterns = [
    path('add_product/', views.add_product, name='add_product'),
    path('list_products/', views.list_products, name='list_products'),
    path('update_product/<int:product_id>', views.update_product, name='update_product'),
    path('delete_product/<int:product_id>', views.delete_product, name='delete_product'),
    path('add_producer/', views.redirect_add_producer_it, name='add_producer'),
    path('add_producer/<str:country>', views.add_producer, name='add_producer'),
]
