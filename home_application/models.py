# -*- coding: utf-8 -*-


from django.db import models

#宿主机信息
class Script(models.Model):
    name = models.CharField(u'脚本名称', max_length=200)
    content = models.CharField(u'内容', max_length=10240)
    default_params = models.CharField(u'默认参数', max_length=1024)
    remark = models.CharField(u'说明', max_length=1024)

    class Meta:
        verbose_name = u'脚本'
        verbose_name_plural = u'脚本'
