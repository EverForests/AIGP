# 用户表 主要维护用户账号和密码

from django.db import models
from django.utils.translation import gettext_lazy as _

from django.db.models.signals import post_save
from django.dispatch import receiver

class CUser(models.Model):
    username = models.CharField(verbose_name=_('UserName'), max_length=150, db_index=True, unique=True)
    password = models.CharField(verbose_name=_('PassWord'), max_length=128)
    create_date = models.DateTimeField(verbose_name=_('Create Date'), auto_now_add=True)

    def __str__(self):
        return self.username # 管理界面add函数的返回值

    class Meta:
        ordering = ['-create_date']
        verbose_name = "user"  # 单文件量词
        verbose_name_plural = "users" # 多文件量词