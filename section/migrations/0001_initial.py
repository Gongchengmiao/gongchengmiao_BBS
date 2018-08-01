# Generated by Django 2.0.6 on 2018-08-01 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionAdministrator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'forum-admin',
            },
        ),
        migrations.CreateModel(
            name='SectionForum',
            fields=[
                ('section_id', models.AutoField(primary_key=True, serialize=False)),
                ('brief', models.CharField(default=None, max_length=140, null=True)),
                ('types', models.CharField(choices=[('g', 'group'), ('f', 'forum'), ('s', 'sub')], max_length=1)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, default='django-db-models-fields-charfield', max_length=500)),
                ('status', models.BooleanField(default=False)),
                ('display_order', models.CharField(choices=[('tim', 'time'), ('pop', 'popularity'), ('tit', 'title')], max_length=3)),
                ('posts', models.IntegerField(default=0)),
                ('todayposts', models.IntegerField(default=0)),
                ('follower_num', models.IntegerField(default=0)),
                ('block', models.CharField(choices=[('a', 'A区: 部门组织'), ('b', 'B区: 信息论坛'), ('c', 'C区: 我们的家'), ('d', 'D区: 出国留学'), ('e', 'E区: 学术科学'), ('f', 'F区: 文化艺术'), ('g', 'G区: 休闲感性'), ('h', 'H区: 体育健身'), ('i', 'I区: 瀚海特区'), ('j', 'J区: 本站系统')], max_length=1)),
                ('lastpostid', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='article.ArticlePost')),
            ],
            options={
                'verbose_name': 'forum',
                'verbose_name_plural': 'forums',
            },
        ),
    ]
