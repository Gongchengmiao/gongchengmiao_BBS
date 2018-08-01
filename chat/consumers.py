from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import ChatGroup, ChatLog
from channels.db import database_sync_to_async
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope['user']
        self.room_group_name = 'chat_%s' % self.room_name

        self.group, created = await self.get_channel(self.room_name)

        if created:
            await self.add_user_into_channel(self.group, self.user)
            # self.group.chat_users.add(self.user)
        elif self.user in self.group.chat_users.all():
            pass
        else:
            await self.add_user_into_channel(self.group, self.user)
            # self.group.chat_users.add(self.user)


        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        chatlog_list = await self.get_chatlogs(self.group)

        for chatlog_ in reversed(chatlog_list):
            await self.send(text_data=json.dumps({
                'message': chatlog_.chat_text,
                'user': chatlog_.chat_speaker.username,
                'time': chatlog_.chat_time.strftime("%Y-%m-%d %H:%M:%S"),
                'is_user': self.user.username == chatlog_.chat_speaker.username,
            }))



    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            text = self.user.username + ': ' + message

            await self.add_chatlog(self.group, self.user, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': self.user.username,
                    'time': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
        except json.JSONDecodeError:
            if(text_data == '/plaese/send/me/the/log'):
                chatlog_list = await self.get_chatlogs(self.group)

                for chatlog_ in reversed(chatlog_list):
                    await self.send(text_data=json.dumps({
                        'message': chatlog_.chat_text,
                        'user': chatlog_.chat_speaker.username,
                        'time': chatlog_.chat_time.strftime("%Y-%m-%d %H:%M:%S"),
                        'is_user': self.user.username == chatlog_.chat_speaker.username,
                    }))

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        time = event['time']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'time': time,
            'is_user': self.user.username == user,
        }))

    @database_sync_to_async
    def get_channel(self, room_name):
        return ChatGroup.objects.get_or_create(channel_name=room_name)

    @database_sync_to_async
    def add_user_into_channel(self, group, user):
        return group.chat_users.add(user)

    @database_sync_to_async
    def add_chatlog(self, group, speak, message):
        chat_log = ChatLog()
        chat_log.chat_group = group
        chat_log.chat_speaker = speak
        chat_log.chat_text = message
        chat_log.save()

    @database_sync_to_async
    def get_chatlogs(self, group):
        return ChatLog.objects.filter(chat_group=group).order_by('-chat_time')[0:50]
