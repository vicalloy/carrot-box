import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Permission
from django.conf import settings as django_settings

AUTH_USER_MODEL = getattr(django_settings, 'AUTH_USER_MODEL', 'auth.User')


class CarrotDepartment(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=50, blank=True)
    parent = models.ForeignKey(
        'CarrotDepartment', blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='sub_departments',
        verbose_name='Parent Department')
    # all parent node, include self
    parents = models.ManyToManyField(
        'CarrotDepartment', verbose_name='All parents department',
        related_name='all_sub_departments',
        editable=False, blank=True)
    leader = models.ForeignKey(
        AUTH_USER_MODEL, blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name="department_master_user")
    permissions = models.ManyToManyField(
        Permission, blank=True)
    oid = models.IntegerField('Order', default=999)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (
            self.uuid,
        )

    def get_parents(self):
        department = self
        parent = department.parent
        parents = [department]
        while parent:
            parents.append(parent)
            department = parent
            parent = department.parent
        return parents

    def update_parents(self):
        old_parents = set(self.parents.all())
        new_parents = set(self.get_parents())
        if old_parents == new_parents:
            return
        self.parents.set(new_parents)
        for d in self.sub_departments.all():
            d.update_parents()

    def save(self, *args, **kwargs):
        if self.parent == self:
            self.parent = None
        super().save(*args, **kwargs)
        self.update_parents()


class CarrotRole(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=50, blank=True)
    users = models.ManyToManyField(
        AUTH_USER_MODEL, blank=True,
        related_name='roles',
    )
    permissions = models.ManyToManyField(
        Permission, blank=True)
    oid = models.IntegerField('Order', default=999)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (
            self.uuid,
        )


class CarrotUserMixin(models.Model):
    full_name = models.CharField(max_length=255, blank=True)
    post = models.CharField(max_length=255, blank=True)
    department_id = models.PositiveIntegerField(null=True, blank=True)
    # department = models.ForeignKey(  # will get error `Can't resolve dependencies`
    #     CarrotDepartment,
    #     on_delete=models.SET_NULL,
    #     null=True, blank=True)
    leader = models.ForeignKey(
        AUTH_USER_MODEL, blank=True, null=True,
        on_delete=models.SET_NULL,
        verbose_name='Leader')

    def get_department(self):
        if self.department_id:
            return CarrotDepartment.objects.filter(pk=self.department_id).first()
        return None

    class Meta:
        abstract = True


class CarrotUser(CarrotUserMixin, AbstractUser):

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = self.username
        super().save(*args, **kwargs)
