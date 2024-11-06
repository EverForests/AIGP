from django.contrib import admin
from .models import CUser

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'create_date')

    '''10 items per page'''
    list_per_page = 10
    
admin.site.register(CUser, CustomUserAdmin)