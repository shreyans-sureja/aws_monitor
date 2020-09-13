from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('monitor/', include('health_monitor.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('fork/',include('reporter.urls'))
]