from django.contrib import admin
from .models import UserTable, Otp


# Register your models here.
class username(admin.ModelAdmin):
    list_display = ['id', 'firstName', 'search_id']


admin.site.register(UserTable, username)
admin.site.register(Otp)

