import uuid

from authentication.models import User
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from organizations.models import Organization, OrganizationUser


class ForUser(models.Manager):
    def for_user(self, user):
        
        org_id = OrganizationUser.objects.get(user=user).organization_id
        return self.get_queryset().filter(organization_id=org_id)

class Vendor(models.Model):
    street_address = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="")
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='Vendor_org', \
        help_text='Organization ID')

    created_by = models.ForeignKey(to=User, on_delete=models.PROTECT, null=False, blank=True, related_name='Vendor_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(to=User, on_delete=models.PROTECT, null=True, blank=True, related_name='Vendor_updated_by')
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = ForUser()

    class Meta:
        indexes = [
            models.Index(fields=['organization', 'created_by']),
        ]

    def __repr__(self):
        return '<Audit {}>'.format(self.city)

class DocumentItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documentId = models.IntegerField(null= False)
    inventoryId = models.IntegerField(null= False)
    name = models.CharField(max_length=250, blank=False, null=False, \
        unique=False, db_index=False, verbose_name='Description', help_text='รายละเอียด')
    
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