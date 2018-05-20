from django.db import models


# Create your models here.


class post(models.Model):
    moderate = models.ForeignKey(post_moderate, unique= True)

    first = models.BooleanField();
    author_name = models.CharField(max_length=15)
    post_title = models.CharField(max_length=80)
    pub_date = models.DateTimeField(auto_now_add = True, editable=True)
    anonymous = models.BooleanField(default=False)


class post_moderate(models.Model):
    status = models.BooleanField(default = True)

class thread(models.Model):
    moderate = models.ForeignKey(thread_moderate, unique=True)

    subject = models.CharField(max_length=80)
    dateline = models.DateTimeField(auto_now_add=True, editable=True)
    lastpost = models.DateTimeField(auto_now=True, null=True)
    views = models.IntegerField(default=0)
    replies = models.IntegerField(default=0)
    recommend_add = models.IntegerField(default=0)
    recommend_sub = models.IntegerField(default=0)

    heats = models.IntegerField(default=0)
    favtimes = models.IntegerField(default=0)
    sharetimes = models.IntegerField(default=0)
    hidden = models.BooleanField(default=False)

class thread_moderate(models.Model):
    status = models.BooleanField(default=True)


