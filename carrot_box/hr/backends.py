# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission
from django.db.models import Q


class BPMModelBackend(ModelBackend):

    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous() or obj is not None:
            return set()
        if not hasattr(user_obj, '_perm_cache'):
            user_obj._perm_cache = self.get_user_permissions(user_obj)
            user_obj._perm_cache.update(self.get_group_permissions(user_obj))
            user_obj._perm_cache.update(self.get_role_permissions(user_obj))
            user_obj._perm_cache.update(self.get_department_permissions(user_obj))
        return user_obj._perm_cache

    def get_role_permissions(self, user_obj, obj=None):
        return self._get_permissions(user_obj, obj, 'role')

    def _get_role_permissions(self, user_obj):
        return Permission.objects.filter(role__staff__user=user_obj)

    def get_department_permissions(self, user_obj, obj=None):
        return self._get_permissions(user_obj, obj, 'department')

    def _get_department_permissions(self, user_obj):
        departments = [user_obj.staff.department]
        departments.extend(user_obj.staff.department.parents.all())
        for d in user_obj.staff.departments.all().distinct():
            departments.extend(d.parents.all())
        departments = set(departments)
        return Permission.objects.filter(department__in=departments)

    def _get_group_permissions(self, user_obj):
        user_groups_field = get_user_model()._meta.get_field('groups')
        user_groups_query = 'group__%s' % user_groups_field.related_query_name()
        qparam = Q(**{user_groups_query: user_obj})
        qparam = qparam | Q(group__groupuser__user=user_obj)
        qparam = qparam | Q(group__groupuser__role__staff__user=user_obj)
        return Permission.objects.filter(qparam)
