from django.db import models

# 用户主表
class common_member(models.Model):
    uid = models.IntegerField(max_length=12, primary_key=True)
    email = models.EmailField()
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    status = models.BooleanField()  #判断用户是否已经删除 1=未删除 0=删除
    email_status = models.BooleanField() #email是否经过验证 1=验证通过 0=未验证
    avatarstatus = models.BooleanField() #是否有头像 1=已上传 0=未上传
    adminid = models.IntegerField(max_length=1) #管理组id 1=管理员 2=超级版主 3=版主
    regdate = models.DateField() #注册时间
    newpm = models.IntegerField(max_length=6) #新短消息数量
    newprompt = models.IntegerField(max_length=6) #新提醒数目
    accessmasks = models.BooleanField() #访问权限
    allowadmincp = models.BooleanField() #管理权限
    freeze = models.BooleanField() #是否被冻结

    def __str__(self):
        return self.username


#用户操作日志表
class common_member_action_log(models.Model):
    id = models.IntegerField(max_length=256, primary_key=True)
    uid = models.ForeignKey(common_member, on_delete=models.CASCADE(), to_field=common_member.uid, db_constraint=True)
    action = models.IntegerField(max_length=5)
    dateline = models.TimeField()

    def __str__(self):
        return self.uid, self.action, self.dateline
