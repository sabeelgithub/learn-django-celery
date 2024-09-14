from django.db import models
import uuid

class Tip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tip_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):  
       return f'{self.tip_name}'

