
from django.db import models
from django.contrib.auth.models import User
from chat.service.utils import file_upload_path

class Chatroom(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name='chatrooms')

class Message(models.Model):
    room = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to=file_upload_path) 

    def __str__(self):
        return f"Attachment for Message ID: {self.message}"
