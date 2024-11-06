from django.contrib import admin
from .models import ImgInfo

# Register your models here.
class ImgInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image', 'username', 'create_date', 'flag')

    '''10 items per page'''
    list_per_page = 10
    
admin.site.register(ImgInfo, ImgInfoAdmin)