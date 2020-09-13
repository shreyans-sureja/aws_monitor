from django.urls import path, include
from rest_framework import routers
from . import views


urlpatterns = [
    path('metrics/<str:id>/',views.get_metrics),
    path('metadata/<str:id>/', views.get_metadata)
]