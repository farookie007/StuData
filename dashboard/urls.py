from django.urls import path

from .views import dashboard, refresh




app_name = 'dashboard'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('refresh/', refresh, name='refresh'),
]