from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'',views.InstanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('records/<str:id>/', views.get_data)
]