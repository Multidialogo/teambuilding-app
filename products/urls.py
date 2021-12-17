from django.urls import path

from products import views

urlpatterns = [
    path('add/', views.add_product, name='add_product'),
    path('list/', views.list_products, name='list_products'),
    path('update/<int:prod_id>', views.update_product, name='update_product'),
    path('delete/<int:prod_id>', views.delete_product, name='delete_product'),
    path('add_option/', views.add_product_purchase_option, name='add_prod_purchase_opt'),
    path('add_option/<int:prod_id>', views.add_product_purchase_option, name='add_prod_purchase_opt'),
    path('list_options/', views.list_product_purchase_options, name='list_prod_purchase_opt'),
    path('list_options/<int:prod_id>', views.list_product_purchase_options, name='list_prod_purchase_opt'),
    path('update_option/<int:prod_option_id>', views.update_product_purchase_option, name='update_prod_purchase_opt'),
    path('delete_option/<int:prod_option_id>', views.delete_product_purchase_option, name='delete_prod_purchase_opt'),
    path('add_producer/', views.redirect_add_producer_it, name='add_producer'),
    path('add_producer/<str:country>', views.add_producer, name='add_producer'),
]
