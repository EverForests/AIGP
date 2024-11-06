from django.db import models
from django.utils.translation import gettext_lazy as _
from CustomUser.models import CUser

class UInfo(models.Model):
    username = models.ForeignKey(CUser, verbose_name=_('username'), on_delete=models.CASCADE, related_name='uinfos', to_field='username', db_column='username')
    photo = models.ImageField(verbose_name=_('photo') ,upload_to='images/photo/', null=True, blank=True)
    followerCount = models.IntegerField(verbose_name=_('followercount'), default=0)

    def __str__(self):
        return str(self.username) # 管理界面add函数的返回值

    class Meta:
        verbose_name = "uinfo"  # 单文件量词
        verbose_name_plural = "uinfos" # 多文件量词