from django.urls import path

from .views import upload_result_view, manual_upload_view




app_name = 'results'

urlpatterns = [
    path('upload/', upload_result_view, name='upload'),
    path('man-upload/', manual_upload_view, name='manual_upload'),
]