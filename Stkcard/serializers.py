from rest_framework import serializers

from .models import TRANSACTION_TYPE, MovementTransaction, Product


class MovementTransactionCreateSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(source="product.sku")
    
    class Meta:
        model = MovementTransaction
        fields = (
            'id',
            'product',
            'sku',
            'quantity',
            'transactionType',
            'created_by',
            'transactionDate',
            )
        read_only_fields = ('id', 'product', 'sku', 'transactionDate')

        extra_kwargs = {
            "sku":  {"required": True},
            "transactionType": {"required": True},
            "quantity": {"required": True},
        }

    def validate(self, attrs):
        sku = attrs.get('product').get('sku')
        quantity = attrs.get('quantity', 0)
        transactionType = attrs.get('transactionType', 0)
        if transactionType==TRANSACTION_TYPE[0][0]:
            quantity= -1 * quantity

        product_by_sku = Product.objects.filter(sku=sku).first()
        if product_by_sku:
            return {
                'product': product_by_sku,
                'quantity': quantity,
                'transactionType': transactionType,
        }
        else:
            raise serializers.ValidationError({'message':'Sku does not exist'})

        return super().validate(attrs)


class MovementTransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MovementTransaction
        fields = (
            'id',
            'product',
            'quantity',
            'transactionType',
            'created_by',
            'transactionDate',
            )
        read_only_fields = ('id', 'created_by','transactionDate')
