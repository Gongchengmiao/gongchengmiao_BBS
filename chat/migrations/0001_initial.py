<<<<<<< HEAD
# Generated by Django 2.0.6 on 2018-08-03 06:20
=======
# Generated by Django 2.0.6 on 2018-08-03 04:47
>>>>>>> b21599d3c6da51e946a04de765e40a0cdf5aeb0c

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='ChatLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_text', models.CharField(max_length=256)),
                ('chat_time', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('chat_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.ChatGroup')),
            ],
        ),
    ]
