from django.urls import path
from orders import views


urlpatterns = [
    path('<int:product_id>', views.purchase, name='purchase'),
    path('success/', views.purchase_success, name='purchase_success'),
]