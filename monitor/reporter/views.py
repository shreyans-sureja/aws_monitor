from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import api_view
from health_monitor.models import instance
import boto3
from datetime import datetime as dt, timedelta

date = dt.today() - timedelta(days=1)
year = date.year
month = date.month
day = date.day

@csrf_exempt
@api_view(['GET', 'POST'])
def index(request,id):

    atts = request.data['attributes']

    try:
        instanc = instance.objects.get(instance_id=id)
        response = {}

        cloudwatch = boto3.client('cloudwatch', region_name=instanc.region_name,
                                  aws_access_key_id= instanc.access_key,
                                  aws_secret_access_key=instanc.secret_access_key)

        attributes = ["CPUUtilization", "DiskReadOps", "DiskWriteOps", "NetworkIn", "NetworkOut"]



        for att in atts:
            query = cloudwatch.get_metric_statistics(Namespace='AWS/EC2',
                                                     MetricName=att,
                                                     Dimensions=[{'Name': 'InstanceId',
                                                                  'Value': id, }],
                                                     StartTime=dt(year, month, day, 00, 00, 00),
                                                     EndTime=dt(year, month, day + 1, 23, 59, 59),
                                                     Period=3600,
                                                     Statistics=['Average', 'Minimum', 'Maximum'])

            if att in attributes:
                response[att] = query
            else:
                response[att] = None

        return JsonResponse(response)
    except:
        return JsonResponse({"message" : "invalid request!" })


