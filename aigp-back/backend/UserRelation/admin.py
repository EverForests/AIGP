from django.contrib import admin
from .models import Follow

# Register your models here.
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followed', 'create_date')

    '''10 items per page'''
    list_per_page = 10
    
admin.site.register(Follow, FollowAdmin)