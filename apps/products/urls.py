from django.urls import path

from . import views

urlpatterns = [
    path('manage/list/', views.list_manage, name='products-list-manage'),
    path('manage/add/', views.add, name='products-add'),
    path('manage/edit/<int:pk>', views.edit, name='products-edit'),
    path('manage/delete/<int:pk>', views.delete, name='products-delete'),
    # path('manage/producers/list/', views.add_product, name='products-producers-list-manage'),
    # path('manage/producers/add/', views.add_product, name='products-producers-add'),
    # path('manage/producers/edit/<int:pk>', views.add_product, name='products-producers-edit'),
    # path('manage/producers/delete/<int:pk>', views.add_product, name='products-producers-delete'),
]
