# Generated by Django 2.0.7 on 2018-07-29 01:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_remove_comment_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='commentator',
            field=models.CharField(default='MrWho', max_length=90),
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='pid',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
