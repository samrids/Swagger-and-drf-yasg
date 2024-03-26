from app.models import DocumentItem, Vendor
from rest_framework import serializers


class VendorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vendor
        fields = (
            'id',
            'street_address',
            'city',
            # 'organization',
            'created_by',
            'updated_by',
            )
        read_only_fields = ('id', 'created_by', 'updated_by',)

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
            'updated_by',
            )
        read_only_fields = ('id', 'sync_at','created_by')

class DocumentItemUpdSerializer(serializers.ModelSerializer):

    # def __init__(self, *args, **kwargs):
    #     kwargs['partial'] = True
    #     super(DocumentItemUpdSerializer, self).__init__(*args, **kwargs)
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
            'updated_by',
            )
        extra_kwargs = {
            'id': {'required': True},
            'documentId':{'required': False},
            'inventoryId':{'required': False},
            'name':{'required': True},
        }
        read_only_fields = ('id', 'sync_at','created_by','updated_by')
