from django.db import models
from gongchengmiao_BBS import settings
from slugify import slugify
from django.urls import reverse
# Create your models here.


class SectionForum(models.Model):
    section_id = models.AutoField(primary_key=True)  # 论坛id
    # section_up_id = models.IntegerField(default=None, null=True)  # 上级论坛id
    types_choices = (
        ('g', 'group'),
        ('f', 'forum'),
        ('s', 'sub')
    )
    brief = models.CharField(max_length=140, default=None, null=True)
    types = models.CharField(max_length=1, choices=types_choices)  # 论坛类型
    name = models.CharField(max_length=50, unique=True)  # 论坛名
    slug = models.SlugField(max_length=500, default=slugify(str(name)), allow_unicode=True)
    status = models.BooleanField(default=False)
    display_order_choices = (
        ('tim', 'time'),
        ('pop', 'popularity'),
        ('tit', 'title')
    )
    display_order = models.CharField(max_length=3, choices=display_order_choices)
    posts = models.IntegerField(default=0) # 帖子数量
    todayposts = models.IntegerField(default=0)
    lastpostid = models.ForeignKey('article.ArticlePost', null=True, default=None, on_delete=models.CASCADE)
    follower_num = models.IntegerField(default=0)
    block_choices = (
        ('a', u'A区: 部门组织'),
        ('b', u'B区: 信息论坛'),
        ('c', u'C区: 我们的家'),
        ('d', u'D区: 出国留学'),
        ('e', u'E区: 学术科学'),
        ('f', u'F区: 文化艺术'),
        ('g', u'G区: 休闲感性'),
        ('h', u'H区: 体育健身'),
        ('i', u'I区: 瀚海特区'),
        ('j', u'J区: 本站系统'),
    )
    block = models.CharField(max_length=1, choices=block_choices)


    class Meta:
        verbose_name = 'forum'
        verbose_name_plural = 'forums'

    def __str__(self):
        return self.name

    def save(self, *args, **kargs):  # ④
        self.slug = slugify(self.name)  # ⑤
        super(SectionForum, self).save(*args, **kargs)

    def get_url(self):  # ⑥
        return reverse("section_all", args={self.slug})



# class Forum_attachemnt(models.Model):
#     pass
    #aid = models.IntegerField(primary_key=True)  # 附件id
    #tid = models.IntegerField(default=0)
    #pid = models.ForeignKey('article.forum_post', null=True, on_delete=models.CASCADE)
    #uid = models.ForeignKey('user.common_member', null=True, on_delete= models.CASCADE)
    # uploadTime = models.DateTimeField(auto_now_add=True)  # 上传时间
    # Automatically set the field to now when the object is first created.
    # If you want to be able to modify this field, set the following instead of auto_now_add=True:
    #  For DateField: default=date.today - from datetime.date.today()
    #  For DateTimeField: default=timezone.now - from django.utils.timezone.now()
    # file = models.FileField(upload_to='attachment/%Y/%m/%d/')  # 具体路径之后设置
    # remote = models.BooleanField(default=False)   # 是否远程存储
    # description = models.CharField(max_length=200)  # 附件描述
    # readperm = models.IntegerField()  # 读取权限
    # 考虑改成外键

class SectionAdministrator(models.Model):
    forum_administrator_fk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    forum_fk = models.ForeignKey(SectionForum, on_delete=models.CASCADE)
    # Authorization = models.ForeignKey('Grant', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'forum-admin'







