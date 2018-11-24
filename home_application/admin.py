# -*- coding: utf-8 -*-

# import from apps here


# import from lib
# ===============================================================================
# from django.contrib import admin
# from apps.__.models import aaaa
#
# admin.site.register(aaaa)
# ===============================================================================


from django.contrib import admin
from home_application.models import Script
admin.site.register(Script)

#@admin.register(SettingProperty)
#class SettingAdmin(admin.ModelAdmin):
#    list_display = ('name','value')
#    list_filter = ('name',)
#    search_fields = ('name',)