from rest_framework import serializers
from product.models.product import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'price',
            'active',
            'category',
        ]

    def create(self, validated_data):
        categories_data = validated_data.pop('category')
        product = Product.objects.create(**validated_data)
        product.category.set(categories_data)
        return product
