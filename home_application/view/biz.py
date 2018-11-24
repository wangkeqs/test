#!/usr/bin/env
# -*- coding:utf-8 -*-

# @auther : wangke
# @date   : 2018-11-24

from common.mymako import render_mako_context, render_json
from blueking.component.shortcuts import get_client_by_request
from common.log import logger
from home_application import models


def search(request):
    return render_mako_context(request, '/home_application/search.html')


def search_biz(request):
    client = get_client_by_request(request)
    business_list=client.cc.search_business()
    print business_list
    data = business_list['data']['info']
    print data
    return render_json(dictionary={"data": data})


def search_host(request):
    bk_biz_id = request.GET.get('bk_biz_id')
    vm = request.GET.get('vm')#vm:1.查宿主机，2查虚拟机，3查所有虚拟机
    os = request.GET.get('os')#os:1.linux，2windows
    ip = request.GET.get('ip')
    ip_flag = "bk_host_innerip"#内网查询IP
    #ip_flag = request.GET.get('ip_flag')
    # if ip_flag is 1:ip_flag = "bk_host_innerip"
    # elif ip_flag is 2:ip_flag = "bk_host_outerip"
    # else:ip_flag = "bk_host_innerip|bk_host_outerip"
    client = get_client_by_request(request)
    if not vm is None:
        data = create_search_vm_by_host(ip,vm,client)
        return render_json(dictionary={"data": data})
    elif not ip is None:
        req_data = create_search_ip(ip,0,ip_flag,os)
        host_list = client.cc.search_host(req_data)
    elif not os is None:
        req_data = create_search_os(os)
        host_list = client.cc.search_host(req_data)
    elif not bk_biz_id is None:
        req_data = create_search_condition("bk_biz_id", bk_biz_id,"biz")
        host_list = client.cc.search_host(req_data)
    else:
        host_list = client.cc.search_host()
    data = host_list['data']['info']
    count = host_list['data']['count']
    return render_json(dictionary={"data":data,"count":count})


#创建主机查询条件
def create_search_condition(filed,value,bk_obj_id):
    req_data = {}
    condition = [{"field": filed, "operator": "$eq", "value": value}]
    req_data['page'] = {"start": 0, "limit": 100}
    req_data['condition'] = [{"bk_obj_id": bk_obj_id, "condition": [condition]},
                             {"bk_obj_id": "host", "fields": [], "condition": []},
                             {"bk_obj_id": "module", "fields": [], "condition": []},
                             {"bk_obj_id": "set", "fields": [], "condition": []}]
    return req_data


#根据操作系统类型查询条件
def create_search_os(os):
    req_data = {}
    condition = {"field": "bk_os_type", "operator": "$eq", "value": os}
    req_data['condition'] = [{"bk_obj_id": "host", "condition": [condition]},
                             {"bk_obj_id": "biz", "fields": [], "condition": []},
                             {"bk_obj_id": "module", "fields": [], "condition": []},
                             {"bk_obj_id": "set", "fields": [], "condition": []}]
    req_data['page'] = {"start": 0, "limit": 100}
    return req_data

#根据宿主机---虚拟机互查条件
def create_search_vm_by_host(ip,vm,client):
    req_data = {}
    #   vm:1.查宿主机，2查虚拟机，3查所有虚拟机
    if vm == '1':
        condition = {"field": "bk_host_innerip", "operator": "$eq", "value": ip}
        req_data['condition'] = [{"bk_obj_id": "host","fields": [],"condition": [condition]},
                                 {"bk_obj_id": "biz","fields": [],"condition":[]},
                                 {"bk_obj_id": "module","fields": [],"condition":[]},
                                 {"bk_obj_id": "set","fields": [],"condition":[]}]
        req_data['page'] = {"start": 0, "limit": 100}
        host_list = client.cc.search_host(req_data)
        host_list = host_list['data']['info']
    elif vm == '2':
        condition = {"field": "host_machine_ip", "operator": "$eq", "value": ip}
        req_data['condition'] = [{"bk_obj_id": "host", "fields": [], "condition": [condition]},
                                 {"bk_obj_id": "biz", "fields": [], "condition": []},
                                 {"bk_obj_id": "module", "fields": [], "condition": []},
                                 {"bk_obj_id": "set", "fields": [], "condition": []}]
        req_data['page'] = {"start": 0, "limit": 100}
        host_list = client.cc.search_host(req_data)
        host_list = host_list['data']['info']
    else:
        #condition = {"field": "host_machine_ip", "operator": "$neq", "value": ""}
        req_data['condition'] = [{"bk_obj_id": "host", "fields": [], "condition": []},
                                 {"bk_obj_id": "biz", "fields": [], "condition": []},
                                 {"bk_obj_id": "module", "fields": [], "condition": []},
                                 {"bk_obj_id": "set", "fields": [], "condition": []}]
        req_data['page'] = {"start": 0, "limit": 100}
        old_host_list = client.cc.search_host(req_data)
        old_host_list = old_host_list['data']['info']
        host_list = []
        for key in range(len(old_host_list)):
            host_lists = old_host_list[key]['host']
            machine_list = host_lists.get('host_machine_ip', None)
            if not machine_list is None:
                if not machine_list is u'':
                    host_list.append(old_host_list[key])
            else:
                continue
    return host_list


#根据IP查询条件
def create_search_ip(ip,exact,flag,os):
    req_data = {}
    if not os is None:
        condition = {"field": "bk_os_type", "operator": "$eq", "value": os}
        req_data['condition'] = [{"bk_obj_id": "host", "condition": [condition]},
                             {"bk_obj_id": "biz", "fields": [], "condition": []},
                             {"bk_obj_id": "module", "fields": [], "condition": []},
                             {"bk_obj_id": "set", "fields": [], "condition": []}]
    req_data['page'] = {"start": 0, "limit": 100}
    req_data['ip'] = {"data": [ip], "exact": exact, "flag": flag}
    return req_data


#更新主机信息
def update_host(request):
    update_value = request.GET.get("update_value")
    client = get_client_by_request(request)
    data={"bk_host_name":update_value}
    data = client.cc.update_host(data)
    return render_json(dictionary={"data": data})


#获取主机详细信息
def get_host_base_info(request):
    client = get_client_by_request(request)
    bk_host_id = request.GET.get("bk_host_id")
    data={"bk_host_id": bk_host_id}
    client.cc.get_host_base_info(data)
    return render_json(dictionary={"data": data})

