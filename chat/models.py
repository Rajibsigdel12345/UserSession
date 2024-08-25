from django.db import models
from authentication.models import User
from uuid import uuid4

# Create your models here.
class Connection(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE , related_name='receiver')
    sender = models.ForeignKey(User, on_delete=models.CASCADE , related_name='sender')
    connection_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('receiver', 'sender')
        constraints = [
            models.CheckConstraint(
                check=~models.Q(sender = models.F('receiver')) , name='prevent_self_connection'
            )
        ]
    
    def __str__(self):
        return self.connection_id

class Groups(models.Model):
    name = models.CharField(max_length=100)
    room_id= models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ManyToManyField(User)
    
    def __str__(self):
        return self.room_id
