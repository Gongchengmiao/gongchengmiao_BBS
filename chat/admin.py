from django.contrib import admin
from .models import ChatGroup, ChatLog

# Register your models here.


class ChatGroupAdmin(admin.ModelAdmin):
    list_display = ('channel_name',)


class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('chat_group', 'chat_text')


admin.site.register(ChatGroup, ChatGroupAdmin)

admin.site.register(ChatLog, ChatLogAdmin)

