from django.urls import path
from . import views

urlpatterns = [
    path('', views.SensorDataView.as_view(), name='home'),
]
