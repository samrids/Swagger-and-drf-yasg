from rest_framework import serializers

from app.models import DocumentItem


class DocumentItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DocumentItem
        fields = (
            'id',
            'documentId',
            'inventoryId',
            'name',
            'isSync',
            'sync_at',
            'created_by',
            )
        read_only_fields = ('id', 'sync_at',)