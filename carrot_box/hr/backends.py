from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission


class CarrotModelBackend(ModelBackend):

    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()
        if not hasattr(user_obj, '_perm_cache'):
            user_obj._perm_cache = super().get_all_permissions(user_obj)
            user_obj._perm_cache.update(self.get_role_permissions(user_obj))
            user_obj._perm_cache.update(self.get_department_permissions(user_obj))
        return user_obj._perm_cache

    def get_role_permissions(self, user_obj, obj=None):
        return self._get_permissions(user_obj, obj, 'role')

    def _get_role_permissions(self, user_obj):
        return Permission.objects.filter(carrotrole__users=user_obj)

    def get_department_permissions(self, user_obj, obj=None):
        return self._get_permissions(user_obj, obj, 'department')

    def _get_department_permissions(self, user_obj):
        department = user_obj.get_department()
        if not department:
            return set()
        departments = department.parents.all()
        return Permission.objects.filter(carrotdepartment__in=departments)
