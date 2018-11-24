#!/usr/bin/env
# -*- coding:utf-8 -*-

# @auther : zhang_zhenqi
# @date   : 2018-09-05 14:07
# @blog   : https://www.wolfpacksoft.com/wordpress/zhang_zhenqi
# @email  : zhang_zhenqi@wolfpacksoft.com
from common.mymako import render_mako_context
from home_application import celery_tasks
def test(request):
    return render_mako_context(request,"/home_application/test.html")

def scanTask(request):
    celery_tasks.scanTask()

def powerShellStatusCheckTask(request):
    celery_tasks.powerShellStatusCheckTask()

def buildHyperVVmInfoTask(request):
    celery_tasks.buildHyperVVmInfoTask()

def checkPowerShellStatusResultTask(request):
    celery_tasks.checkPowerShellStatusResultTask()

def checkSetExecutionPolicyTask(request):
    celery_tasks.checkSetExecutionPolicyTask()