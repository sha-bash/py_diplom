from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Shop, Category, Product, ProductInfo, Order, OrderItem, Contact

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'url']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'shops']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category']

class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    shop = ShopSerializer(read_only=True)

    class Meta:
        model = ProductInfo
        fields = ['id', 'product', 'shop', 'quantity', 'price', 'price_rrc']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'user', 'city', 'street', 'house', 'structure', 
                 'building', 'apartment', 'phone']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_info', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    ordered_items = OrderItemSerializer(many=True, read_only=True)
    total_sum = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'dt', 'state', 'ordered_items', 'total_sum']

    def get_total_sum(self, obj):
        return sum(item.quantity * item.product_info.price for item in obj.ordered_items.all())
