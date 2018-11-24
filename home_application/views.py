# -*- coding: utf-8 -*-

from common.mymako import render_mako_context, render_json
from blueking.component.shortcuts import get_client_by_request
from django.http import JsonResponse
import base64
from common.log import logger
from home_application import models


def index(request):
    return render_mako_context(request, '/home_application/index.html')

def search_biz(request):
    client = get_client_by_request(request)
    business_list=client.cc.search_business()
    data = business_list['data']['info']
    result = []
    for item in data:
        my_map={'id':item['bk_biz_id'], 'text':item['bk_biz_name']}
        result.append( my_map )
    print result
    #return render_json(dictionary={"data": result})
    return render_json(result)

def search_script(request):
    script_list = models.Script.objects.all()
    result=[]
    for script in script_list:
        my_map = {'id': script.id, 'text': script.script_name}
        result.append(my_map)
    return render_json(dictionary={"data": result})

def search_host(request):
    bk_biz_id = request.GET.get('biz_id')
    client = get_client_by_request(request)
    if not bk_biz_id is None:  # 业务查询
        req_data = create_search_condition("bk_biz_id", bk_biz_id, "biz")
        #req_data = create_search_condition("bk_biz_id", 2, "biz")
        host_list = client.cc.search_host(req_data)
    data = host_list['data']['info']
    count = host_list['data']['count']
    return render_json(dictionary={"data": data, "count": count})

#根据业务查询
def create_search_condition(filed,value,bk_obj_id):
    req_data = {}
    condition = [{"field": filed, "operator": "$eq", "value": value}]
    req_data['condition'] = [{"bk_obj_id": bk_obj_id, "condition": [condition]},
                             {"bk_obj_id": "host", "fields": [], "condition": []},
                             {"bk_obj_id": "module", "fields": [], "condition": []},
                             {"bk_obj_id": "set", "fields": [], "condition": []}]
    req_data['page'] = {"start": 0, "limit": 100}
    return req_data

# 执行脚本
# ip_addrs: 选择的ip列表
def execute_script(request):
    client = get_client_by_request(request)
    script_name = request.POST.get('script_name')
    bk_biz_id = request.POST.get('biz_id')
    script_obj = models.Script.objects.filter(name=script_name)
    ip_addrs = request.POST.get('ip_addrs')
    script_param = request.POST.get('script_param')
    result = {}
    try:
        ip_list = []
        for ip in ip_addrs:
            ip_list.append( {'bk_cloud_id': 0, 'ip': ip} )
        req_data = {}
        req_data['bk_biz_id'] = bk_biz_id
        req_data['account'] = 'wangke'
        # 手动输入脚本内容
        script_content = ''
        req_data['script_content'] = base64.encodestring(script_obj.content)
        if script_param:
            req_data['script_param'] = base64.encodestring(script_param)
        else:
            req_data['script_param'] = base64.encodestring(script_obj.default_params)
        # 1(shell脚本)、2(bat脚本)、3(perl脚本)、4(python脚本)、5(Powershell脚本)
        req_data['script_type'] = 1
        req_data['ip_list'] = ip_list
        res = client.job.fast_execute_script(req_data)
        if res['result']:
            job_instance_name = res['data']['job_instance_name']
            job_instance_id = res['data']['job_instance_id']
            result['sucess']=True
    except Exception as e:
        result['sucess'] = False
    return render_json(dictionary={"data": result})


# 查询脚本执行的结果
def serach_script_result(request):
    client = get_client_by_request(request)
    bk_biz_id = request.POST.get('biz_id')
    job_instance_id = request.POST.get('job_instance_id')
    result = {}
    try:
        if bk_biz_id is None:
            return None
        if job_instance_id is None:
            return None
        req_data = {}
        req_data['bk_biz_id'] = bk_biz_id
        req_data['job_instance_id'] = job_instance_id
        res = client.job.get_job_instance_log(req_data)
        if res['result']:
            result = res['data']
    except Exception as e:
        logger.error(e.message)

    return render_json(dictionary={"data": result})


def api_test(request):
    data = {'result': 'true', 'message': 'hello', 'data': 'world'}
    return render_json(dictionary={"data": data})




