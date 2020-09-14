from background_task import background
from health_monitor.models import instance
from datetime import datetime, time, timedelta
from .models import records

import boto3

@background(schedule=3600)
def start():

    instances = instance.objects.all()

    for inst in instances:
        db_time = inst.updated_at + timedelta(seconds=inst.time)
        db_time = db_time.replace(tzinfo=None)
        curr_time = datetime.now()

        # curr_time += timedelta(days=1)

        curr_time = curr_time.replace(tzinfo=None)

        if db_time <= curr_time:
            query = get_data(inst)
            print(query)

            try:
                record = records()
                record.instance_id = inst.instance_id
                record.timestamp = query['Timestamp']
                record.avg_usage = query['Average']
                record.max_usage = query['Maximum']
                record.min_usage = query['Minimum']
                record.save()
            except:
                print("something went wrong!")

            inst.updated_at = datetime.now()
            inst.save()


def get_data(instanc):
    date = datetime.today() - timedelta(days=1)
    year = date.year
    month = date.month
    day = date.day

    cloudwatch = boto3.client('cloudwatch', region_name=instanc.region_name,
                                  aws_access_key_id= instanc.access_key,
                                  aws_secret_access_key=instanc.secret_access_key)

    id = instanc.instance_id

    query = cloudwatch.get_metric_statistics(Namespace='AWS/EC2',
                                                MetricName="CPUUtilization",
                                                Dimensions=[{'Name': 'InstanceId',
                                                            'Value': id, }],
                                                StartTime=datetime(year, month, day, 00, 00, 00),
                                                EndTime=datetime(year, month, day + 1, 23, 59, 59),
                                                Period=3600,
                                                Statistics=['Average', 'Minimum', 'Maximum'])


    x = None
    result = {}
    for datapoint in query['Datapoints']:
        if x is None:
            x = datapoint['Timestamp']
            result = datapoint
        elif x < datapoint['Timestamp']:
            x = datapoint['Timestamp']
            result = datapoint

    return result