from django.db import models
from django.utils.translation import gettext_lazy as _
from CustomUser.models import CUser

class ImgInfo(models.Model):
    username = models.ForeignKey(CUser, verbose_name=_('username'), on_delete=models.CASCADE, related_name='imginfos', to_field='username', db_column='username')
    title = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(verbose_name=_('image') ,upload_to='images/goe/', null=True, blank=True)
    create_date = models.DateTimeField(verbose_name=_('Create Date'), auto_now_add=True)
    flag = models.BooleanField(verbose_name=_('is_goe'), default=False)  # 是否为二次开发图像

    def __str__(self):
        return str(self.username) # 管理界面add函数的返回值

    class Meta:
        verbose_name = "imginfo"  # 单文件量词
        verbose_name_plural = "imginfos" # 多文件量词