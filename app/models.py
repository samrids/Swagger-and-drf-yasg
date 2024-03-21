import uuid

from django.db import models


class DocumentItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documentId = models.IntegerField(null= False)
    inventoryId = models.IntegerField(null= False)
    name = models.CharField(max_length=250, blank=False, null=False, unique=False, db_index=False)
    
    isSync = models.BooleanField(null=False, default=False)
    sync_at = models.DateTimeField(auto_now_add=True)

    created_by = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['documentId', 'inventoryId']),
        ]

    def __str__(self):
        return self.documentId