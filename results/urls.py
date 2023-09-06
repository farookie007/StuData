from django.urls import path

from .views import upload_result_view, CourseDetailView, CourseUpdateView




app_name = 'results'

urlpatterns = [
    path('upload/', upload_result_view, name='upload'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('course/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
]