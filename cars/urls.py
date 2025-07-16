from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.car_create, name='car_create'),

    path('cars/<int:pk>/edit/', views.CarUpdateView.as_view(), name='car_edit'),

    path('delete/<int:id>/', views.car_delete, name='car_delete'),

]
