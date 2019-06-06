from django.urls import path

from . import views


app_name = 'trades'


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('history/', views.history, name='history'),

    path('trade/add/', views.edit, name='add'),
    path('trade/edit/<int:pk>/', views.edit, name='edit'),
]
