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


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        queryset=User.objects.all(),
    )
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(read_only=True)

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


class OrderItemSerializer(serializers.ModelSerializer):
    shoe_name = serializers.CharField(source='variant.shoe.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'quantity', 'price', 'variant', 'shoe_name']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'customer', 'message', 'is_read', 'created_at']


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


class CartItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
