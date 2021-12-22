from django.urls import path

from . import views

urlpatterns = [
    path('detail/<int:pk>', views.add, name='events-detail'),
    path('list/next/', views.list_upcoming, name='events-list-next'),
    path('list/history/', views.list_history, name='events-list-history'),
    path('manage/list/', views.list_manage, name='events-list-manage'),
    path('manage/add/', views.add, name='events-add'),
    path('manage/edit/<int:pk>', views.edit, name='events-edit'),
    path('manage/delete/<int:pk>', views.delete, name='events-delete'),
]
