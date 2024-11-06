from django.contrib import admin
from .models import UInfo

# Register your models here.
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('username', 'photo', 'followerCount')

    '''10 items per page'''
    list_per_page = 10
    
admin.site.register(UInfo, UserInfoAdmin)