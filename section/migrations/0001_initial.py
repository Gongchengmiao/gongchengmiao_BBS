# Generated by Django 2.0.6 on 2018-06-09 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum_admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'forum-admin',
            },
        ),
        migrations.CreateModel(
            name='Forum_forum',
            fields=[
                ('fid', models.IntegerField(primary_key=True, serialize=False)),
                ('fup', models.IntegerField(default=None, null=True)),
                ('types', models.CharField(choices=[('g', 'group'), ('f', 'forum'), ('s', 'sub')], max_length=1)),
                ('name', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=False)),
                ('displayorder', models.CharField(choices=[('tim', 'time'), ('pop', 'popularity'), ('tit', 'title')], max_length=3)),
                ('styleid', models.IntegerField(default=0)),
                ('threads', models.IntegerField(default=0)),
                ('posts', models.IntegerField(default=0)),
                ('todayposts', models.IntegerField(default=0)),
                ('allowEmoijs', models.BooleanField(default=True)),
                ('allowHtml', models.BooleanField(default=True)),
                ('allowImgcode', models.BooleanField(default=True)),
                ('allowMediacode', models.BooleanField(default=True)),
                ('allowAnonymous', models.BooleanField(default=False)),
                ('allowEditRules', models.BooleanField(default=True)),
                ('checkPosts', models.BooleanField(default=False)),
                ('lastpostid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.forum_post')),
            ],
            options={
                'verbose_name': 'forum',
                'verbose_name_plural': 'forums',
            },
        ),
        migrations.CreateModel(
            name='Forum_userAct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
