from django.db import models


# Create your models here.

# class forum_post_moderate(models.Model):
#     status = models.BooleanField(default = True)

# 一般帖子信息
class forum_post(models.Model):
    # moderate = models.ForeignKey(forum_post_moderate, unique= True)
    # first = models.BooleanField();
    pid = models.IntegerField(primary_key=True)
    author_name = models.CharField(max_length=64)
    post_title = models.CharField(max_length=256)
    pub_date = models.DateTimeField(auto_now_add = True, editable=True)
    text = models.TextField()
    # anonymous = models.BooleanField(default=False)

    def __str__(self):
        return self.post_title


# 学校通告信息
class forum_school_info(models.Model):
    pid = models.IntegerField(primary_key=True)
    author_name = models.CharField(max_length=64)
    post_title = models.CharField(max_length=256)
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    text = models.TextField()

    def __str__(self):
        return self.post_title


# 帖子浏览量信息
class forum_read(models.Model):
    pid = models.ForeignKey(forum_post, on_delete=models.CASCADE)
    read_time = models.IntegerField(default=0)


# class forum_thread_moderate(models.Model):
#     status = models.BooleanField(default=True)

# class forum_thread(models.Model):
#     moderate = models.ForeignKey(forum_thread_moderate, unique=True)
#
#     subject = models.CharField(max_length=80)
#     dateline = models.DateTimeField(auto_now_add=True, editable=True)
#     lastpost = models.DateTimeField(auto_now=True, null=True)
#     views = models.IntegerField(default=0)
#     replies = models.IntegerField(default=0)
#     recommend_add = models.IntegerField(default=0)
#     recommend_sub = models.IntegerField(default=0)
#
#     heats = models.IntegerField(default=0)
#     favtimes = models.IntegerField(default=0)
#     sharetimes = models.IntegerField(default=0)
#     hidden = models.BooleanField(default=False)

