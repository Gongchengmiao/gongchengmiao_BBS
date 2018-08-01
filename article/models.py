from django.db import models


# Create your models here.


from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from slugify import slugify
from django.urls import reverse
from DjangoUeditor.models import UEditorField

#from django.template.defaultfilters import slugify
#from uuslug import slugify

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column


class ArticlePost(models.Model):
    pid = models.AutoField(primary_key=True, auto_created=True)  # 增加一个主键
    is_school_info = models.BooleanField(default=False)  # 是否公告

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    ueditor_body = UEditorField(width=600, height=300, null=True, toolbars="full", imagePath="images/", filePath="files/",
                                upload_settings={"imageMaxSize": 1204000}, settings={}, verbose_name='内容')

    isElite = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now_add=True, editable=True, db_index=True)

    section_belong_fk = models.ForeignKey('section.SectionForum', on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=500, default=slugify(str(title)), allow_unicode=True)
    comment_counter = models.IntegerField(default=0)

    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="articles_like", blank=True)

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes')

    def __str__(self):
        return self.title

    def save(self, *args, **kargs):  # ④
        self.slug = slugify(self.title)  # ⑤
        super(ArticlePost, self).save(*args, **kargs)

    def get_url(self):  # ⑥
        return reverse("article_detail", args=[self.pid, self.slug])

    @property
    def total_likes(self):
        """
        Likes for the company
        :return: Integer: Likes for the company
        """
        return self.likes.count()
        #return int(3)


# 帖子浏览量信息
class PostRead(models.Model):
    user_fk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_fk = models.ForeignKey(ArticlePost, on_delete=models.CASCADE)
    read_time = models.IntegerField(default=0)

class Comment(models.Model):
    article = models.ForeignKey(ArticlePost, related_name='comments', on_delete=models.CASCADE, null=True)
    commentator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ueditor_body = UEditorField(width=300, height=200, null=True, toolbars="mini", imagePath="images/", filePath="files/",
                                upload_settings={"imageMaxSize": 1204000}, settings={}, verbose_name='内容')
    created = models.DateTimeField(auto_now_add=True)
    counter = models.IntegerField()
    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.article.title






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













