from django.urls import path

from . import views

urlpatterns = [
    path('manage/list', views.list_manage, name='products-list-manage'),
    path('manage/add', views.add, name='products-add'),
    path('manage/edit/<int:pk>', views.edit, name='products-edit'),
    path('manage/delete/<int:pk>', views.delete, name='products-delete'),
    path('manage/producer/list', views.producer_list_manage, name='producer-list-manage'),
    path('manage/producers/add', views.producer_add, name='product-producer-add'),
    path('manage/producers/add/<str:country>', views.producer_add, name='product-producer-add'),
    path('manage/producers/delete/<int:pk>', views.producer_delete, name='product-producer-delete'),
    path('manage/producers/edit/<int:pk>', views.producer_edit, name='product-producer-edit'),
    path('manage/producers/edit/<int:pk>/<str:country>', views.producer_edit, name='product-producer-edit'),
    # path('manage/producers/list/', views.add_product, name='products-producers-list-manage'),
    # path('manage/producers/add/', views.add_product, name='products-producers-add'),
    # path('manage/producers/edit/<int:pk>', views.add_product, name='products-producers-edit'),
    # path('manage/producers/delete/<int:pk>', views.add_product, name='products-producers-delete'),
]
