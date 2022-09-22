from rest_framework import serializers
from .models import Product, Order


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'price', 'description')


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    item = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ('userid', 'orderid', 'item', 'price')

