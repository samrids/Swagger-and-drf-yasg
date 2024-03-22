import uuid

from django.db import models

from authentication.models import User


class DocumentItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documentId = models.IntegerField(null= False)
    inventoryId = models.IntegerField(null= False)
    name = models.CharField(max_length=250, blank=False, null=False, unique=False, db_index=False)
    
    isSync = models.BooleanField(null=False, default=False)
    sync_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(to=User, on_delete=models.PROTECT, null=False, blank=True, related_name='DocumentItem_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(to=User, on_delete=models.PROTECT, null=True, blank=True, related_name='DocumentItem_updated_by')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['documentId', 'inventoryId']),
        ]

    def __str__(self):
        return self.documentId