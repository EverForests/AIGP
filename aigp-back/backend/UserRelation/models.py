from django.db import models
from django.utils.translation import gettext_lazy as _
from CustomUser.models import CUser

class Follow(models.Model):
    follower = models.ForeignKey(CUser, verbose_name=_('follower'), to_field='username', db_column='follower', related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(CUser, verbose_name=_('followed'), to_field='username', db_column='followed', related_name='followers', on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name='Create Date', auto_now_add=True)

    def __str__(self):
        return str(self.id) # 管理界面add函数的返回值
    
    class Meta:
        verbose_name = "relation"  # 单文件量词
        verbose_name_plural = "relations" # 多文件量词