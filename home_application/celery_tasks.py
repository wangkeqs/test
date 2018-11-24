# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
from celery import task
from home_application.models import Script
from home_application.util import  host_util
from common.log import logger
from celery.task import periodic_task
from celery.schedules import crontab
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')




# #启动powershell状态检查
# def powerShellStatusCheckTask():
#     host_set = HostInfo.objects.filter(host_status=0,host_type=0)
#     if host_set:
#         for host_info in host_set:
#             jobInfo = host_util.doCheckExecutionPolicy(host_info)
#             if jobInfo:
#                 taskInfo = TaskInfo()
#                 taskInfo.task_type = 1
#                 taskInfo.task_name = u'检查powershell是否支持命令'
#                 taskInfo.job_instance_id = jobInfo['job_instance_id']
#                 taskInfo.job_instance_name = jobInfo['job_instance_name']
#                 taskInfo.host_info = host_info
#                 taskInfo.save()
#             else:
#                 logger.error(u'doCheckExecutionPolicy failed,hostip:%s' %host_info.bk_host_ip)



