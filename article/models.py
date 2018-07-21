from django.db import models


# Create your models here.


from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from slugify import slugify
from django.urls import reverse

#from django.template.defaultfilters import slugify
from uuslug import slugify

# # 一般帖子信息
# class forum_post(models.Model):
#     # moderate = models.ForeignKey(forum_post_moderate, unique= True)
#     # first = models.BooleanField();
#     pid = models.IntegerField(primary_key=True)
#     author_name = models.CharField(max_length=64)
#     post_title = models.CharField(max_length=256)
#     pub_date = models.DateTimeField(auto_now_add = True, editable=True)
#     text = models.TextField()
#     # anonymous = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.post_title


class ArticleColumn(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='article_column')
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column


class ArticlePost(models.Model):
    pid = models.IntegerField(primary_key=True)  # 增加一个主键
    is_school_info = models.BooleanField(default=False)  # 是否公告

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="article")
    title = models.CharField(max_length=200)
    body = models.TextField()
    isElite = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)

    section_belong_fk = models.ForeignKey('section.SectionForum', on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=500, default=slugify(str(title)), allow_unicode=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kargs):  # ④
        self.slug = slugify(self.title)  # ⑤
        super(ArticlePost, self).save(*args, **kargs)

    def get_absolute_url(self):  # ⑥
        return reverse("article:article_detail", args=[self.pid, self.slug])

    def get_url_path(self):
        return reverse("article:list_article_detail", args=[self.pid, self.slug])


# 帖子浏览量信息
class PostRead(models.Model):
    user_fk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_fk = models.ForeignKey(ArticlePost, on_delete=models.CASCADE)
    read_time = models.IntegerField(default=0)

# class forum_post_moderate(models.Model):
#     status = models.BooleanField(default = True)

# # 一般帖子信息
# class forum_post(models.Model):
#     # moderate = models.ForeignKey(forum_post_moderate, unique= True)
#     # first = models.BooleanField();
#     # pid = models.IntegerField(primary_key=True)
#     author_name = models.CharField(max_length=64)
#     post_title = models.CharField(max_length=256)
#     pub_date = models.DateTimeField(auto_now_add = True, editable=True)
#     text = models.TextField()
#     # anonymous = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.post_title
#
#
# # 学校通告信息
# class forum_school_info(models.Model):
#     # pid = models.IntegerField(primary_key=True)
#     author_name = models.CharField(max_length=64)
#     post_title = models.CharField(max_length=256)
#     pub_date = models.DateTimeField(auto_now_add=True, editable=True)
#     text = models.TextField()
#
#     def __str__(self):
#         return self.post_title
#













