from django.urls import path, include

urlpatterns = [
    path('users/', include('teambuilding.site.urls_users')),
    path('auth/', include('teambuilding.site.urls_auth')),
]
