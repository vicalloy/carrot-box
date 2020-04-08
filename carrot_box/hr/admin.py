from django.contrib import admin

from .models import CarrotDepartment
from .models import CarrotRole
from .models import CarrotUser


@admin.register(CarrotUser)
class CarrotUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'post', 'get_department', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
    autocomplete_fields = ('leader', )  # 'department',


@admin.register(CarrotDepartment)
class CarrotDepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'parent', 'leader', 'oid', 'is_active',)
    search_fields = ('code', 'name')
    ordering = ('oid',)
    filter_horizontal = ('permissions', )
    autocomplete_fields = ('parent', 'parents', 'leader', )


@admin.register(CarrotRole)
class CarrotRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'oid', 'is_active',)
    search_fields = ('code', 'name')
    ordering = ('oid',)
    filter_horizontal = ('permissions',)
    autocomplete_fields = ('users', )
