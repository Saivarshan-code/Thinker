from django.contrib import admin
from .models import userprofile
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    # fields
    # search_fields = ['user']
    list_filter = ['std']
    list_display = ['user','std']
    # list_editable


admin.site.register(userprofile,UserProfileAdmin)
