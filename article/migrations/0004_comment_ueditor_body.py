# Generated by Django 2.0.7 on 2018-07-28 09:38

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20180728_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='ueditor_body',
            field=DjangoUeditor.models.UEditorField(null=True, verbose_name='内容'),
        ),
    ]
