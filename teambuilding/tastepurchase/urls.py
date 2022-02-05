from django.urls import path, include

urlpatterns = [
    path('events/', include('teambuilding.tastepurchase.urls_event')),
    path('products/', include('teambuilding.tastepurchase.urls_product')),
]
