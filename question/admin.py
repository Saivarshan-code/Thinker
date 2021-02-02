from django.contrib import admin
from .models import question,comment

# Register your models here.
admin.site.register(question)
admin.site.register(comment)

# @admin.site(comment)
# class commentAdmin(admin.ModelAdmin):
#     ordering = ('question',)
#
#     def formfield_for_dbfield(self, db_field, request, **kwargs):
#         if db_field.name == 'question':
#             kwargs['strip'] = False
#         return super().formfield_for_dbfield(db_field, request, **kwargs)
