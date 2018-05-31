from django.db import models


# 用户主表
class common_member(models.Model):

    uid = models.IntegerField(max_length=12, primary_key=True)
    email = models.EmailField()
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    status = models.BooleanField()   # 判断用户是否已经删除 1=未删除 0=删除
    email_status = models.BooleanField()  # email是否经过验证 1=验证通过 0=未验证
    avatarstatus = models.BooleanField()  # 是否有头像 1=已上传 0=未上传
    adminid = models.IntegerField(max_length=1)  # 管理组id 1=管理员 2=超级版主 3=版主
    regdate = models.DateField()  # 注册时间
    newpm = models.IntegerField(max_length=6)  # 新短消息数量
    newprompt = models.IntegerField(max_length=6)  # 新提醒数目
    accessmasks = models.BooleanField()  # 访问权限
    allowadmincp = models.BooleanField()  # 管理权限
    freeze = models.BooleanField()  # 是否被冻结

    def __str__(self):
        return self.username


# 用户操作日志表
class common_member_action_log(models.Model):
    id = models.IntegerField(max_length=256, primary_key=True)
    uid = models.ForeignKey(common_member, on_delete=models.CASCADE, to_field=common_member.uid, db_constraint=True)
    action = models.IntegerField(max_length=5)  # 动作, 具体以后再定义
    dateline = models.TimeField()  # 操作时间

    def __str__(self):
        return self.uid, self.action, self.dateline


# 用户统计表
class common_member_count(models.Model):
    uid = models.ForeignKey(common_member, on_delete=models.CASCADE, to_field=common_member.uid, db_constraint=True)
    posts = models.IntegerField(max_length=12)  # 帖子数
    threads = models.IntegerField(max_length=12)  # 主题数
    digestposts = models.IntegerField(max_length=10)  # 精华数
    doings = models.IntegerField(max_length=10)  # 记录数
    blogs = models.IntegerField(max_length=10)  # 日志数
    albums = models.IntegerField(max_length=10)  # 相册数
    sharings = models.IntegerField(max_length=14)  # 分享数
    attachsize = models.IntegerField(max_length=15)  # 上传附件占用的空间
    views = models.IntegerField(max_length=15)  # 空间查看数
    oltime = models.IntegerField(max_length=12)  # 在线时间
    todayattachs = models.IntegerField(max_length=12)  # 当天上传附件数
    todayattachsize = models.IntegerField(max_length=15)  # 当天上传附件容量
    blacklist = models.IntegerField(max_length=12)  # 黑名单

    def __str__(self):
        return self.uid, common_member.objects.get(uid=self.uid)


# 用户惩罚操作表
class member_crime(models.Model):
    cid = models.IntegerField(max_length=12, primary_key=True)  # 自增id
    uid = models.ForeignKey(common_member, on_delete=models.CASCADE, to_field=common_member.uid, db_constraint=True)
    operatorid = models.ForeignKey(common_member, on_delete=models.CASCADE,
                                   to_field=common_member.uid, db_constraint=True)  # 进行惩罚操作的用户id
    action = models.ForeignKey(common_member_action_log, on_delete=models.CASCADE,
                               to_field=common_member_action_log.action, db_constraint=True)  # 惩罚行为
    reason = models.TextField()  # 惩罚理由
    dateline = models.TimeField()  # 惩罚操作时间

    def __str__(self):
        return self.uid, self.action


# 用户论坛字段表
class common_member_field_forum(models.Model):
    STUDENT = 'ST'
    TEACHER = 'TE'

    groupterms_choice = (
        (STUDENT, 'student'),
        (TEACHER, 'teacher'),
    )

    uid = models.ForeignKey(common_member, on_delete=models.CASCADE, to_field=common_member.uid, db_constraint=True)
    groupterms = models.CharField(max_length=2, choices=groupterms_choice, default=STUDENT)  # 公共用户组

    def __str__(self):
        return self.uid, self.get_groupterms_display()


# 用户家园字段表
class common_member_field_home(models.Model):
    uid = models.ForeignKey(common_member, on_delete=models.CASCADE, to_field=common_member.uid, db_constraint=True)
    spacename = models.CharField(max_length=256)
    domain = models.CharField(max_length=15)  # 空间绑定二级域名 home





