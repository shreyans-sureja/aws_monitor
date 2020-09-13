from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .models import instance
from .serializers import InstanceSerializer

def index(request):
    return HttpResponse("Hello, world!")

class InstanceViewSet(viewsets.ModelViewSet):
    queryset = instance.objects.all().order_by('instance_id')
    serializer_class = InstanceSerializer

    def create(self,request):
        print(request.data['description'])

        x = self.serializer_class(data = request.data)

        if x.is_valid():
            self.perform_create(x)

        return HttpResponse("lololol")
