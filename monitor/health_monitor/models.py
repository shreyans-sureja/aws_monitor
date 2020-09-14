from django.db import models

class instance(models.Model):
    description = models.CharField(max_length=50)
    instance_id = models.CharField(max_length=50)
    region_name = models.CharField(max_length=50)
    access_key = models.CharField(max_length=500)
    secret_access_key = models.CharField(max_length=500,default="")
    thresold = models.CharField(max_length=5,default="100")
    time = models.IntegerField(default=3600)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description