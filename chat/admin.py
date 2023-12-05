from django.contrib import admin
from chat.entity.models import Chatroom, Message, Attachment
# Register your models here.


admin.site.register(Chatroom)
admin.site.register(Message)
admin.site.register(Attachment)