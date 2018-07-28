from django.db import models
from user.models import common_member

# Create your models here.


class ChatGroup(models.Model):
    channel_name = models.CharField(max_length=256)
    chat_users = models.ManyToManyField(common_member)

    def __str__(self):
        return self.channel_name


class ChatLog(models.Model):
    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    chat_speaker = models.ForeignKey(common_member, on_delete=models.CASCADE)
    chat_text = models.CharField(max_length=256)
    chat_time = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return "{}  {}".format(self.chat_group, self.chat_text)


