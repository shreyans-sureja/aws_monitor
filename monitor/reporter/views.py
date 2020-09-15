import boto3
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import api_view
from health_monitor.models import instance
from datetime import datetime as dt, timedelta
from operator import itemgetter

date = dt.today() - timedelta(days=1)
year = date.year
month = date.month
day = date.day

@csrf_exempt
@api_view(['POST'])
def get_metrics(request,id):

    atts = request.data['attributes']

    try:
        instanc = instance.objects.all().filter(instance_id=id).first()
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


@csrf_exempt
@api_view(['GET'])
def get_metadata(request,id):

    try:
        instanc = instance.objects.all().filter(instance_id=id).first()
        response = {}

        ec2 = boto3.resource('ec2', region_name=instanc.region_name,
                                  aws_access_key_id=instanc.access_key,
                                  aws_secret_access_key=instanc.secret_access_key)


        inst = ec2.Instance(id)

        response["instance-id"] = inst.id
        response["instance-type"] = inst.instance_type
        response["public-ipv4"] = inst.instance_id
        response["hostname"] = inst.root_device_name

        client = boto3.client('ec2', region_name=instanc.region_name,
                            aws_access_key_id=instanc.access_key,
                            aws_secret_access_key=instanc.secret_access_key)

        temp = client.describe_images(
            Filters=[{
                'Name': 'virtualization-type',
                'Values': ['hvm']
            }],
            Owners=[
                'self'
            ]
        )
        image_details = sorted(temp['Images'], key=itemgetter('CreationDate'), reverse=True)
        ami_id = image_details[0]['ImageId']
        response["ami-id"] = ami_id

        return JsonResponse(response)
    except:
        return JsonResponse({"message" : "something went wrong, check instance id again!"})
