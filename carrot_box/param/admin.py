from django.contrib import admin

from .models import ParamType, Param


class ParamInline(admin.TabularInline):
    raw_id_fields = ('parent', 'param_type')
    model = Param


@admin.register(ParamType)
class ParamTypeAdmin(admin.ModelAdmin):
    search_fields = ('code', 'name', )
    list_display = ('code', 'name', 'oid', 'is_active',)
    inlines = [
        ParamInline,
    ]


@admin.register(Param)
class ParamAdmin(admin.ModelAdmin):
    search_fields = ('code', 'name', 'param_type__name', 'param_type__code')
    list_display = ('name', 'param_type', 'code', 'oid', 'is_active',)
    raw_id_fields = ('parent', 'param_type')
    inlines = [
        ParamInline,
    ]
