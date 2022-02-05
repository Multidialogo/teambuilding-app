from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('products/', views.list_all, name='product-list'),
    path('products/purchasable/', views.list_purchasable, name='product-list-purchasable'),
    path('products/add/', views.create, name='product-create'),
    path('products/<int:pk>/edit/', views.update, name='product-update'),
    path('products/<int:pk>/delete/', views.delete, name='product-delete'),
    path('products/<int:pk>/purchase/', views.product_order_create, name='product-order-create'),
    path('products/producers/', views.producer_list_all, name='product-producer-list'),
    path('products/producers/orders/', views.producer_list_purchasable, name='product-producer-list-purchasable'),
    path('products/producers/add/', views.producer_create, name='product-producer-create'),
    path('products/producers/add/<str:country>/', views.producer_create, name='product-producer-create'),
    path('products/producers/<int:pk>/delete/', views.producer_delete, name='product-producer-delete'),
    path('products/producers/<int:pk>/edit/', views.producer_update, name='product-producer-update'),
    path('products/producers/<int:pk>/edit/<str:country>/', views.producer_update, name='product-producer-update'),
    path('products/producers/<int:producer_id>/send-order/', views.producer_order_create, name='product-producer-order-create'),
    path('products/producers/<int:producer_id>/send-order/<str:country>/', views.producer_order_create, name='product-producer-order-create'),
    path('products/<int:product_id>/edit/options/add/', views.purchase_option_create, name='product-purchase-option-create'),
    path('products/_/edit/options/<int:pk>/delete/', views.purchase_option_delete, name='product-purchase-option-delete'),
    path('products/<int:product_id>/edit/options/<int:pk>/delete/', views.purchase_option_delete, name='product-purchase-option-delete'),
    path('products/_/edit/options/<int:pk>/edit/', views.purchase_option_update, name='product-purchase-option-update'),
    path('products/<int:product_id>/edit/options/<int:pk>/edit/', views.purchase_option_update, name='product-purchase-option-update'),
    path('events/', RedirectView.as_view(pattern_name='event-all-list-upcoming')),
    path('events/all/', RedirectView.as_view(pattern_name='event-all-list-upcoming')),
    path('events/all/<int:pk>/', views.event_detail, name='event-detail'),
    path('events/all/upcoming/', views.list_upcoming_events_by_all, name='event-all-list-upcoming'),
    path('events/all/history/', views.list_past_events_by_all, name='event-all-list-history'),
    path('events/user/', views.list_upcoming_events_by_self, name='event-user-list'),
    path('events/user/new/', views.event_create, name='event-create'),
    path('events/user/<int:pk>/edit/', views.event_update, name='event-update'),
    path('events/user/<int:pk>/delete/', views.event_delete, name='event-delete'),
]
