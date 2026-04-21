from rest_framework import serializers
from django.contrib.auth.models import User

from .models import (
    Shoe,
    ShoeImage,
    ShoeVariant,
    Brand,
    Customer,
    PaymentMethod,
    Address,
    Coupon,
    Order,
    OrderItem,
    Notification,
    Review,
    Admin,
    WishlistItem,
    CartItem,
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'first_name', 'last_name']


class ShoeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shoe
        fields = '__all__'


class ShoeImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShoeImage
        fields = '__all__'


class ShoeVariantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShoeVariant
        fields = '__all__'


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Customer
        fields = '__all__'


class PaymentMethodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class CouponSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class AdminSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        queryset=User.objects.all(),
        allow_null=True,
    )

    class Meta:
        model = Admin
        fields = '__all__'


class WishlistItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WishlistItem
        fields = '__all__'


"""class CartItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__' 
"""

class CartItemSerializer(serializers.ModelSerializer):
    shoe_name = serializers.CharField(source='variant.shoe.name', read_only=True)
    price = serializers.FloatField(source='variant.shoe.price', read_only=True)
    color = serializers.CharField(source='variant.color', read_only=True)
    size = serializers.CharField(source='variant.size', read_only=True)
    image = serializers.ImageField(source='variant.shoe.image', read_only=True)
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id', 'variant', 'shoe_name',
            'price', 'quantity',
            'color', 'size', 'image',
            'item_total'
        ]

    def get_item_total(self, obj):
        return obj.total_price