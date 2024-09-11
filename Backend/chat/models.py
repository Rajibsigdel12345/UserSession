from django.db import models
from authentication.models import User
from uuid import uuid4
from .choices import RolesChoices

# Create your models here.
class Connection(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE , related_name='receiver')
    sender = models.ForeignKey(User, on_delete=models.CASCADE , related_name='sender')
    connection_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    connected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('receiver', 'sender')
        constraints = [
            models.CheckConstraint(
                check=~models.Q(sender = models.F('receiver')) , name='prevent_self_connection'
            )
        ]
    
    def __str__(self) -> str:
        return f'{self.connection_id}'

class Messages(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg_author')
    message = models.TextField()
    connection = models.ForeignKey(Connection, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delete_for_author = models.BooleanField(default=False)
    delete_for_receiver = models.BooleanField(default=False)
    delete_for_all = models.BooleanField(default=False)
    
    def __str__(self)-> str:
        return f"{self.author.username} : {self.message[:20]}"

class Groups(models.Model):
    name = models.CharField(max_length=100)
    admin = models.ManyToManyField(User, related_name='admin')
    room_id= models.UUIDField(default=uuid4, editable=False, unique=True)
    
    def __str__(self)-> str:
        return f"{self.room_id}"
class GroupMembers(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='group')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, default='member', choices=RolesChoices.choices)
    messages = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delete_for_author = models.BooleanField(default=False)
    delete_for_all = models.BooleanField(default=False)
    
    def __str__(self)-> str:
        return f"{self.user} in {self.group}"


