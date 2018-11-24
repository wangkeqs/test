# -*- coding: utf-8 -*-

from django.conf.urls import patterns,url,include

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'index'),
    #(r'^biz/', include("home_application.url.biz")),
    (r'^search_biz$','search_biz'),
    (r'^search_script$','search_script'),
    (r'^execute_script$','execute_script'),
    (r'^api/test$','api_test'),
)
