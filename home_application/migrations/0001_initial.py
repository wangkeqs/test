# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u811a\u672c\u540d\u79f0')),
                ('content', models.CharField(max_length=10240, verbose_name='\u5185\u5bb9')),
                ('default_params', models.CharField(max_length=1024, verbose_name='\u9ed8\u8ba4\u53c2\u6570')),
                ('remark', models.CharField(max_length=1024, verbose_name='\u8bf4\u660e')),
            ],
            options={
                'verbose_name': '\u811a\u672c',
                'verbose_name_plural': '\u811a\u672c',
            },
        ),
    ]
