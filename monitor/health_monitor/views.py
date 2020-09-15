import boto3
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .models import instance
from rest_framework.decorators import api_view
from .serializers import InstanceSerializer
from reporter.models import records

def index(request):
    return HttpResponse("Hello, world!")

class InstanceViewSet(viewsets.ModelViewSet):
    queryset = instance.objects.all().order_by('instance_id')
    serializer_class = InstanceSerializer

    def create(self,request):
        x = self.serializer_class(data = request.data)

        if x.is_valid():
            self.perform_create(x)

            alrm = create_alarm(request.data)

            if alrm is True:
                return JsonResponse({"message" : "instance successfully added and alarm created for thresold!"})
            else:
                return JsonResponse({"message" : "Unable to create alarm for thresold, please check params again!"})
        else:
            return JsonResponse({"message": "invalid request!"})



def create_alarm(data):
        instance_id = data['instance_id']
        region = data['region_name']
        access_key = data['access_key']
        secret_access_key = data['secret_access_key']
        thresold = data['thresold']

        cloudwatch = boto3.client('cloudwatch', region_name=region,aws_access_key_id=access_key,aws_secret_access_key=secret_access_key)

        try:
            query = cloudwatch.put_metric_alarm(
                AlarmName='Web_Server_CPU_Utilization',
                ComparisonOperator='GreaterThanThreshold',
                EvaluationPeriods=1,
                MetricName='CPUUtilization',
                Namespace='AWS/EC2',
                Period=3600,
                Statistic='Average',
                Threshold= float(thresold),
                ActionsEnabled=True,
                AlarmDescription='Alarm when server CPU exceeds thresold!',
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    },
                ],
                Unit='Percent'
            )

            if query['ResponseMetadata']['HTTPStatusCode'] != 200:
                return False
            return True
        except:
            return False

@csrf_exempt
@api_view(['GET'])
def get_data(request,id):

    response = []
    try:
        entries = records.objects.all().filter(instance_id=id)
        for entry in entries:
            temp = {}
            temp['Timestamp'] = entry.timestamp
            temp['Average'] = entry.avg_usage
            temp['Maximum'] = entry.max_usage
            temp['Minimum'] = entry.min_usage
            response.append(temp)

        return JsonResponse({"InstanceId" : id , "datapoints" : response})
    except:
        return JsonResponse({"message" : "Invalid request!"})
