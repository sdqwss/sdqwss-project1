from django.utils import timezone
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class Room(models.Model):
    name = models.CharField(max_length=255, blank=True)
    members = models.ManyToManyField(User, related_name='chat_rooms')
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        if self.is_private and self.members.count() == 2:
            users = self.members.all()
            return f"Личный чат: {users[0].username} и {users[1].username}"
        return self.name or "Без названия"

    @classmethod
    def get_private_room(cls, user1, user2):

        rooms = cls.objects.filter(
            is_private=True,
            members=user1
        ).filter(members=user2)

        if rooms.exists():
            return rooms.first()

        room = cls.objects.create(is_private=True)
        room.members.add(user1, user2)
        return room

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE, verbose_name="Комната")
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE, verbose_name="Пользователь")
    content = models.TextField(verbose_name="Сообщение")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время отправки")

    def str(self):
        return f'{self.user.username}: {self.content[:30]}'

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['timestamp']
