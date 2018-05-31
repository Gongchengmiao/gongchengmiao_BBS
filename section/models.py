from django.db import models

# Create your models here.
from django.db import models


class Forum_forum(models.Model):
    fid = models.IntegerField(primary_key=True) # 论坛id
    fup = models.IntegerField(default=None, null=True) # 上级论坛id
    types_choices = (
        ('g', 'group'),
        ('f', 'forum'),
        ('s', 'sub')
    )
    types = models.CharField(max_length=1, choices=types_choices) # 论坛类型
    name = models.CharField(max_length=50) # 论坛名
    status = models.BooleanField(default=False)
    displayorder_choices = (
        ('tim', 'time'),
        ('pop', 'popularity'),
        ('tit', 'title')
    )
    displayorder = models.CharField(max_length=3, choices=displayorder_choices)
    styleid = models.IntegerField(default=0)
    threads = models.IntegerField(default=0)
    posts = models.IntegerField(default=0) # 帖子数量
    todayposts = models.IntegerField(default=0)
    lastpostid = models.ForeignKey('article.forum_post', null=True, on_delete=models.CASCADE)
    allowEmoijs = models.BooleanField(default=True)
    allowHtml = models.BooleanField(default=True)
    allowImgcode = models.BooleanField(default=True)
    allowMediacode = models.BooleanField(default=True)
    allowAnonymous = models.BooleanField(default=False)
    allowEditRules = models.BooleanField(default=True)
    checkPosts = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'forum'
        verbose_name_plural = 'forums'

    def __str__(self):
        return self.name


class Forum_attachemnt(models.Model):
    aid = models.IntegerField(primary_key=True)  # 附件id
    tid = models.IntegerField(default=0)
    pid = models.ForeignKey('article.forum_post',null=True, on_delete=models.CASCADE)
    uid = models.ForeignKey('user.common_member', null=True, on_delete= models.CASCADE)
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

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = 'attachment'
        verbose_name_plural = 'attachments'


class Forum_admin(models.Model):
    #未定义外键
    pass
    #admin = models.ForeignKey('UseId', on_delete=models.CASCADE)
    #forum = models.ForeignKey(Forum_forum, on_delete=models.CASCADE)
    # Authorization = models.ForeignKey('Grant', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.admin)+'-'+str(self.forum)

    class Meta:
        verbose_name = 'forum-admin'


class Forum_userAct(models.Model):
    pass
    # 这个留给用户部分吧233333





