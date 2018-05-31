# Generated by Django 2.0.2 on 2018-05-31 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('section', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='common_member',
            fields=[
                ('uid', models.IntegerField(max_length=12, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('status', models.BooleanField()),
                ('email_status', models.BooleanField()),
                ('avatarstatus', models.BooleanField()),
                ('adminid', models.IntegerField(max_length=1)),
                ('regdate', models.DateField()),
                ('newpm', models.IntegerField(max_length=6)),
                ('newprompt', models.IntegerField(max_length=6)),
                ('accessmasks', models.BooleanField()),
                ('allowadmincp', models.BooleanField()),
                ('freeze', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='common_member_action_log',
            fields=[
                ('id', models.IntegerField(max_length=256, primary_key=True, serialize=False)),
                ('action', models.IntegerField(max_length=5)),
                ('dateline', models.TimeField()),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.common_member')),
            ],
        ),
        migrations.CreateModel(
            name='common_member_star',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='section.Forum_forum')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.common_member')),
            ],
        ),
    ]