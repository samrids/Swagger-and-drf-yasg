from authentication.models import User
from django.db import models


class Color(models.Model):
    name = models.CharField(max_length=100)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True, related_name='Color_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True, related_name='Color_updated_by')
    
    def __str__(self):
        return '{0}'.format( self.name )
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True, related_name='Category_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True, related_name='Category_updated_by')
    
    def __str__(self):
        return '{0}'.format( self.name )
    
class Product(models.Model):
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT)
    sku = models.CharField(max_length=50, null=False, blank=False, unique=True, verbose_name='sku code', db_index=True)
    name = models.CharField(max_length=250, null=False, blank=False, verbose_name='product name')
    color = models.ForeignKey(to=Color, on_delete=models.SET_NULL, null=True)
    quantity = models.SmallIntegerField(null=True, default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True, related_name='Product_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True, related_name='Product_updated_by')

    def __str__(self):
        return '{0}'.format( self.sku )

    class Meta:
        verbose_name = 'Product'
        # ordering = ['sub_category', 'rep_code']

TRANSACTION_TYPE = [
    (0 , 'Decrement'),
    (1 , 'Increment'),
]
class MovementTransaction(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, related_name='MovementTransaction_product')
    quantity = models.SmallIntegerField(null=False, default=1)
    transactionType = models.SmallIntegerField(choices=TRANSACTION_TYPE, null=False, default=1, verbose_name='Transaction type', \
        help_text='0=Decrement, 1=Increment')
    transactionDate = models.DateField(auto_now_add=True, null=False)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True, related_name='MovementTransaction_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True, related_name='MovementTransaction_updated_by')

    def __str__(self):
        return '{0}'.format( self.product )