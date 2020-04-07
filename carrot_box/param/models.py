import uuid
from django.db import models
from lbworkflow.core.datahelper import get_or_create


class ParamType(models.Model):
    code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    oid = models.IntegerField('Order', default=999)
    is_active = models.BooleanField(default=True)

    @classmethod
    def get_all(cls, **kwargs):
        return cls.objects.filter(is_active=True, **kwargs).order_by('oid')

    class Meta:
        ordering = ["oid"]

    def __str__(self):
        return self.name


def create_param_type(*args, **kwargs):
    return get_or_create(ParamType, *args, uid_field_name='code', **kwargs)


class Param(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey(
        'Param',
        on_delete=models.SET_NULL,
        blank=True, null=True)
    param_type = models.ForeignKey(
        ParamType,
        on_delete=models.CASCADE,
        blank=True, null=True)
    code = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)
    oid = models.IntegerField('Order', default=999)
    is_active = models.BooleanField(default=True)

    @classmethod
    def get_all(cls, **kwargs):
        return cls.objects.filter(is_active=True, **kwargs).order_by('oid')

    def natural_key(self):
        return '%s' % self.uuid

    class Meta:
        ordering = ["oid"]

    def __str__(self):
        return self.name


def create_param(*args, **kwargs):
    return get_or_create(Param, *args, **kwargs)
