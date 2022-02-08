from django.urls import path, include

from . import views

urlpatterns = [
    path('events/', include('teambuilding.tastepurchase.urls_event')),
    path('products/', include('teambuilding.tastepurchase.urls_product')),
    path('', views.home, name='taste-purchase-home')
]
