from django.urls import path

from products import views

urlpatterns = [
    path('add_product/', views.add_product, name='add_product'),
    path('list_products/', views.list_products, name='list_products'),
    path('update_product/<int:product_id>', views.update_product, name='update_product'),
    path('delete_product/<int:product_id>', views.delete_product, name='delete_product'),
    path('add_product_flavour/', views.add_product_flavour, name='add_product_flavour'),
    path('add_product_flavour/<int:product_id>', views.add_product_flavour, name='add_product_flavour'),
    path('list_product_flavours/', views.list_product_flavours, name='list_product_flavours'),
    path('list_product_flavours/<int:product_id>', views.list_product_flavours, name='list_product_flavours'),
    path('update_product_flavour/<int:product_flavour_id>', views.update_product_flavour, name='update_product_flavour'),
    path('delete_product_flavour/<int:product_flavour_id>', views.delete_product_flavour, name='delete_product_flavour'),
    path('add_producer/', views.redirect_add_producer_it, name='add_producer'),
    path('add_producer/<str:country>', views.add_producer, name='add_producer'),
]
