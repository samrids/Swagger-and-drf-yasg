import uuid

from authentication.models import User
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from organizations.models import Organization, OrganizationUser


class OrganizationMixin:
    """Mixin used like a SingleObjectMixin to fetch an organization"""

    org_model = Organization
    org_context_name = "organization"

    def get_org_model(self):
        return self.org_model

    def get_context_data(self, **kwargs):
        kwargs.update({self.org_context_name: self.organization})
        return super().get_context_data(**kwargs)

    @cached_property
    def organization(self):
        organization_pk = self.kwargs.get("organization_pk", None)
        return get_object_or_404(self.get_org_model(), pk=organization_pk)

    def get_object(self):
        return self.organization

    get_organization = get_object  # Now available when `get_object` is overridden

class Vendor(OrganizationMixin, models.Model):
    street_address = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="")
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='Vendor_org', \
        help_text='Organization ID')

    created_by = models.ForeignKey(to=User, on_delete=models.PROTECT, null=False, blank=True, related_name='Vendor_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(to=User, on_delete=models.PROTECT, null=True, blank=True, related_name='Vendor_updated_by')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['organization', 'created_by']),
        ]


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