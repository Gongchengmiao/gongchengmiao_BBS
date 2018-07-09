from django.db import models
from gongchengmiao_BBS import settings
from django.utils import timezone
from django.urls import reverse

from django.template.defaultfilters import slugify

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


class ArticleTag(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tag")
    tag = models.CharField(max_length=500)

    def __str__(self):
        return self.tag


class ArticlePost(models.Model):
    pid = models.IntegerField(primary_key=True)  # 增加一个主键
    is_school_info = models.BooleanField(default=False)  # 是否公告

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="article")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn, on_delete=models.CASCADE, related_name="article_column")
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)  # ②
    updated = models.DateTimeField(auto_now=True)
    # users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="articles_like", blank=True)
    # 已经在User的model定义
    article_tag = models.ManyToManyField(ArticleTag, related_name='article_tag', blank=True)

    class Meta:
        ordering = ("-updated",)
        index_together = (('id', 'slug'),)  # ③

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
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name="comments")  # ①
    commentator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)  # ②

    def __str__(self):
        return "Comment by {0} on {1}".format(self.commentator, self.article)



