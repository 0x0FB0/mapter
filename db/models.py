import sys
import uuid

try:
    from django.db import models
except Exception:
    print('Exception: Django Not Found, please install it with "pip install django".')
    sys.exit()

class VPCInstance(models.Model):
    #id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    id = models.CharField(primary_key=True, unique=True, max_length=255, editable=False)
    cidr = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.id

class SubnetInstance(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=255, editable=False)
    vpc = models.ForeignKey(VPCInstance, related_name='subnets', on_delete=models.SET_NULL,
                              null=True, blank=True)
    cidr = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.id

class SecGroupInstance(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=255, editable=False)
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.id

class EC2Instance(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=255, editable=False)
    private = models.CharField(max_length=255)
    public = models.CharField(max_length=255, null=True, blank=True)
    subnet = models.ForeignKey(SubnetInstance, related_name='instances', on_delete=models.SET_NULL,
                              null=True, blank=True)
    secgroups = models.ManyToManyField(SecGroupInstance)
    def __str__(self):
        return self.id

