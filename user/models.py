from django.db import models
from article.models import forum_post, forum_school_info
from section.models import Forum_forum
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from .validators import BbsUsernameValidator
from django.utils.timezone import now


# 用户主表
class common_member(AbstractUser):

    # uid = models.IntegerField(max_length=12, primary_key=True)
    # email = models.EmailField()
    # username = models.CharField(max_length=20, unique=True)
    # password = models.CharField(max_length=20)
    # status = models.BooleanField(default=True)   # 判断用户是否已经删除 1=未删除 0=删除
    portrait = models.ImageField(upload_to='portraits', null=True,blank=True)
    gender_choices = (('m', '男'), ('f', '女'))
    gender = models.CharField(max_length=1, default='m', choices=gender_choices)    # 性别 true为男
    show_gender = models.BooleanField(default=True)  # 是否显示
    profile = models.CharField(default='', max_length=280)
    email_status = models.BooleanField(default=False)  # email是否经过验证 1=验证通过 0=未验证
    username_validator = BbsUsernameValidator
    posts = models.IntegerField(default=0)  # 帖子数
    following = models.IntegerField(default=0)  # 关注者数
    followed = models.IntegerField(default=0)  # 被关注数
    followers = models.ManyToManyField('common_member', symmetrical=False, through='follower_pair')

    def follow_list(self):
        return ','.join([i.username for i in self.followers.all()])

    # avatarstatus = models.BooleanField(default=False)  # 是否有头像 1=已上传 0=未上传
    # accessmasks = models.BooleanField(default=True)  # 访问权限
    # allowadmincp = models.BooleanField(default=False)  # 管理权限
    # freeze = models.BooleanField(default=False)  # 是否被冻结
    pass
    # adminid = models.IntegerField(null=True)  # 管理组id 1=管理员 2=超级版主 3=版主
    # regdate = models.DateField()  # 注册时间
    # newpm = models.IntegerField()  # 新短消息数量
    # newprompt = models.IntegerField()  # 新提醒数目
    def __str__(self):
        return self.username

class follower_pair(models.Model):
    followed = models.ForeignKey(common_member,on_delete=models.CASCADE, related_name='%(class)s_followed')
    by = models.ForeignKey(common_member,on_delete=models.CASCADE, related_name='%(class)s_by')

    #其他属性
    follow_time = models.DateTimeField(auto_now=True)

# 用户邮件验证发送次数表
class common_member_email_send_time(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email_time = models.IntegerField(default=0)  # 邮件发送次数
    last_send_time = models.DateTimeField(auto_now=True)  # 上次发送时间

    def __str__(self):
        return '{} {}'.format(self.user, self.email_time)


# 用户操作日志表
class common_member_action_log(models.Model):
    id = models.IntegerField(primary_key=True)
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_school_info = models.BooleanField(default=False)
    pid = models.ForeignKey(forum_post, null=True, blank=True, on_delete=models.CASCADE)
    spid = models.ForeignKey(forum_school_info, null=True, blank=True, on_delete=models.CASCADE)
    action_choices = (
        ('post', '发帖'),
        ('star', '收藏'),
        ('upload', '上传文件')
    )
    action = models.CharField(max_length=10, choices=action_choices)  # 操作类型
    dateline = models.DateTimeField(auto_now=True)  # 操作时间

    def __str__(self):
        return '{} {} {} {}'.format(self.uid, self.action, self.pid, self.dateline)


# 用户统计表
# (部分合并到用户主表！！！
# class common_member_count(models.Model):
#     uid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     posts = models.IntegerField()  # 帖子数
#     threads = models.IntegerField()  # 主题数
#     digestposts = models.IntegerField()  # 精华数
#     doings = models.IntegerField()  # 记录数
#     blogs = models.IntegerField()  # 日志数
#     albums = models.IntegerField()  # 相册数
#     sharings = models.IntegerField()  # 分享数
#     attachsize = models.IntegerField()  # 上传附件占用的空间
#     views = models.IntegerField()  # 空间查看数
#     oltime = models.IntegerField()  # 在线时间
#     todayattachs = models.IntegerField()  # 当天上传附件数
#     todayattachsize = models.IntegerField()  # 当天上传附件容量
#     blacklist = models.IntegerField()  # 黑名单
#
#     def __str__(self):
#         return '{} {}'.format(self.uid, common_member.objects.get(uid=self.uid))


# 用户惩罚操作表
class member_crime(models.Model):
    # cid = models.IntegerField(max_length=12, primary_key=True)  # 自增id
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_constraint=True)
    action = models.ForeignKey(common_member_action_log, on_delete=models.CASCADE,
                               db_constraint=True)  # 惩罚行为
    reason = models.TextField()  # 惩罚理由
    dateline = models.DateTimeField(auto_now=True)  # 惩罚操作时间

    def __str__(self):
        return '{} {}'.format(self.uid, self.action)


# 用户论坛字段表
class common_member_field_forum(models.Model):
    STUDENT = 'ST'
    TEACHER = 'TE'

    groupterms_choice = (
        (STUDENT, 'student'),
        (TEACHER, 'teacher'),
    )

    uid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    groupterms = models.CharField(max_length=2, choices=groupterms_choice, default=STUDENT)  # 公共用户组

    def __str__(self):
        return "{} {}".format(self.uid, self.get_groupterms_display())


# 用户家园字段表
class common_member_field_home(models.Model):
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    spacename = models.CharField(max_length=256)
    domain = models.CharField(max_length=15)  # 空间绑定二级域名 home


# 用户收藏表
class common_member_star(models.Model):
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_school_info = models.BooleanField(default=False)
    pid = models.ForeignKey(forum_post, null=True, blank=True, on_delete=models.CASCADE)
    spid = models.ForeignKey(forum_school_info, null=True, blank=True, on_delete=models.CASCADE)
    star_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.is_school_info:
            return "{}, {}".format(self.uid, self.spid.pk)
        else:
            return "{}, {}".format(self.uid, self.pid.pk)


