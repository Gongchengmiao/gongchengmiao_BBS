from django.db import models


# Create your models here.


from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from slugify import slugify
from django.urls import reverse


class ArticleColumn(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='article_column')
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column


class ArticlePost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name="article")
    title = models.CharField(max_length=200)
    body = models.TextField()

    slug = models.SlugField(max_length=500)
    slug.allow_unicode = True

    def __str__(self):
        return self.title

    def save(self, *args, **kargs):  # ④
        self.slug = slugify(self.title)  # ⑤
        super(ArticlePost, self).save(*args, **kargs)

    def get_absolute_url(self):  # ⑥
        return reverse("article:article_detail", args=[self.id, self.slug])

    def get_url_path(self):
        return reverse("article:list_article_detail", args=[self.id, self.slug])


class Comment(models.Model):
    article = models.ForeignKey(ArticlePost, related_name='comments', on_delete=models.CASCADE)
    commentator = models.CharField(max_length=90)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "Comment by {0} on {1}".format(self.commentator, self.article)






# class forum_post_moderate(models.Model):
#     status = models.BooleanField(default = True)

# 一般帖子信息
class forum_post(models.Model):
    # moderate = models.ForeignKey(forum_post_moderate, unique= True)
    # first = models.BooleanField();
    # pid = models.IntegerField(primary_key=True)
    author_name = models.CharField(max_length=64)
    post_title = models.CharField(max_length=256)
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    text = models.TextField()
    # anonymous = models.BooleanField(default=False)

    def __str__(self):
        return self.post_title


# 学校通告信息
class forum_school_info(models.Model):
    # pid = models.IntegerField(primary_key=True)
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

