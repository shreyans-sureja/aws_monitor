from django.db import models

class records(models.Model):
    instance_id = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    avg_usage = models.CharField(max_length=100,default="0")
    max_usage = models.CharField(max_length=100,default="0")
    min_usage = models.CharField(max_length=100,default="0")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.instance_id