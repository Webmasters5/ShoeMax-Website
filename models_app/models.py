from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Shoe(models.Model):
    GENDER_CHOICES = [
        ('M', 'Men'),
        ('W', 'Women'),
        ('U', 'Unisex'),
        ('K', 'Kids'),
    ]
    
    CATEGORY_CHOICES = [
        ('running', 'Running'),
        ('sports', 'Sports'),
        ('casual', 'Casual'),
        ('sneakers', 'Sneakers'),
        ('athletic', 'Athletic'),
        ('formal', 'Formal'),
        ('loafers', 'Loafers'),
        ('crocs','Crocs'),
        ('heels','Heels'),
        ('dress pumps','Dress pumps'),
        ('boots', 'Boots'),
        ('sandals', 'Sandals'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    shoe_id = models.AutoField(primary_key=True)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name='shoes')
    #image_url = models.ImageField(upload_to='shoes/')
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:shoe_details', args=[self.shoe_id])

class ShoeImage(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='shoe_images/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Image for {self.shoe.name}'

class ShoeVariant(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, related_name='variants')
    color = models.CharField(max_length=50)
    size = models.IntegerField(validators=[MinValueValidator(35), MaxValueValidator(49)])
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    sku = models.CharField(max_length=100, unique=True, blank=True)
    variant_id = models.AutoField(primary_key=True)

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f'{self.shoe.shoe_id}-{self.color[:3].upper()}-{self.size}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.shoe.name} - {self.color} - {self.size}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['shoe', 'color', 'size'], name='unique_shoe_color_size')
        ]
    
class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField()
    brand_id = models.AutoField(primary_key=True)
    
    def __str__(self):
        return self.name
""" 
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_profile',
        null=True,
        blank=True
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    wishlist_items = models.ManyToManyField(Shoe, through='WishlistItem', related_name='wishlisted_by_customers')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
"""

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    customer_id = models.AutoField(primary_key=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        blank=True
    )
    phone = models.CharField(max_length=15, blank=False, default="")
    mobile = models.CharField(max_length=15, blank=True, default="")
    shipping_address = models.TextField(blank=True, default="")
    billing_address = models.TextField(blank=True, default="")
    credit_card = models.CharField(max_length=16, blank=True, default="")
    theme_preference = models.CharField(
        max_length=10,
        choices=[("light", "Light"), ("dark", "Dark")],
        default="light",
    )
    wishlist_items = models.ManyToManyField(Shoe, through='WishlistItem', related_name='wishlisted_by_customers')

    def __str__(self):
        return self.user.username


"""
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_delivered = models.DateTimeField(null=True, blank=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    shoe_variants = models.ManyToManyField('ShoeVariant', through='OrderItem', related_name='orders')
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    def total_amount(self):
        return self.sub_total + self.shipping_cost - self.discount_amount
    
    def __str__(self):
        return f'Order {self.order_id} - {self.status}'
"""

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    shipping_address = models.TextField(blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.user.username}"
""" 
class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')
    variant = models.ForeignKey('ShoeVariant', on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('order', 'variant')

    def __str__(self):
        return f'OrderItem - {self.variant} x {self.quantity}'
    
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.variant.shoe.price * self.quantity
        super().save(*args, **kwargs)
        self.order.sub_total = sum(item.price for item in self.order.order_items.all()) + self.price
        self.order.save()
"""

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

class Notification(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True, related_name="notifications"
    )

    def __str__(self):
        return f"Notification for {self.customer.user.username}: {self.message[:50]}"

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    order_item = models.OneToOneField('OrderItem', on_delete=models.CASCADE, related_name='review')
    
    def __str__(self):
        return self.title

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admin_profile',
        null=True,
        blank=True
    )
    role = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'Admin {self.admin_id} - {self.role}'

class WishlistItem(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    shoe = models.ForeignKey('Shoe', on_delete=models.CASCADE, related_name='wishlisted_by')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'shoe')

    def __str__(self):
        return f'WishlistItem {self.shoe} for {self.customer}'

""" 
class Coupon(models.Model):
    coupon_id = models.AutoField(primary_key=True)
    promo_code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    percent_off = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)
    exp_date = models.DateTimeField(null=True, blank=True)

    def is_valid(self) -> bool:
        if not self.is_active:
            return False
        if self.exp_date and self.exp_date < timezone.now():
            return False
        return True

    def __str__(self):
        return f'Coupon {self.promo_code} - {self.percent_off}%'
"""

class CartItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cart_items')
    variant = models.ForeignKey(ShoeVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.variant.shoe.price * self.quantity

    def __str__(self):
        return f"{self.variant} (x{self.quantity})"

class PaymentMethod(models.Model):
    card_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='payment_methods')
    card_num = models.CharField(max_length=19)
    exp_date = models.DateField()
    card_type = models.CharField(max_length=50, blank=True)
    holder_name = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        masked = self.card_num[-4:] if self.card_num else '----'
        return f'PaymentMethod {self.card_id} - ****{masked} ({self.holder_name})'


class Address(models.Model):
    addr_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f'Address {self.addr_id} - {self.street}, {self.city} ({self.customer})'

