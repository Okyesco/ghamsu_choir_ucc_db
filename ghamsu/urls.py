from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('form', views.form_view, name='form'),
    path('update/', views.update_view, name='update'),
    path('attendance/', views.attendance_view, name='attendance'),
]