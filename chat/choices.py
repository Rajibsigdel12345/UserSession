from django.db import models

class RolesChoices(models.TextChoices):
    ADMIN = 'admin' , "Admin"
    MEMBER = 'member' , "Member"