from django.urls import path

from . import views

urlpatterns = [
    path('manage/list', views.list_manage, name='product-list-manage'),
    path('manage/add', views.add, name='product-add'),
    path('manage/edit/<int:pk>', views.edit, name='product-edit'),
    path('manage/delete/<int:pk>', views.delete, name='product-delete'),
    path('manage/producer/list', views.producer_list_manage, name='product-producer-list-manage'),
    path('manage/producers/add', views.producer_add, name='product-producer-add'),
    path('manage/producers/add/<str:country>', views.producer_add, name='product-producer-add'),
    path('manage/producers/delete/<int:pk>', views.producer_delete, name='product-producer-delete'),
    path('manage/producers/edit/<int:pk>', views.producer_edit, name='product-producer-edit'),
    path('manage/producers/edit/<int:pk>/<str:country>', views.producer_edit, name='product-producer-edit'),
    path('manage/<int:product_id>/options/add', views.purchase_option_add, name='product-purchase-option-add'),
    path('manage/<int:product_id>/options/delete/<int:pk>', views.purchase_option_delete, name='product-purchase-option-delete'),
    path('manage/<int:product_id>/options/edit/<int:pk>', views.purchase_option_edit, name='product-purchase-option-edit'),
]
