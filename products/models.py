from django.db import models

# Create your models here.
class Shoe(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    size = models.IntegerField()
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    shoe_id = models.AutoField(primary_key=True)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name='shoes')
    image_url = models.ImageField(upload_to='shoes/')
    def __str__(self):
        return self.name

class ShoeVariant(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, related_name='variants')
    color = models.CharField(max_length=50)
    size = models.IntegerField()
    stock = models.IntegerField()
    sku = models.CharField(max_length=100, unique=True)
    variant_id = models.AutoField(primary_key=True)
    def __str__(self):
        return f'{self.shoe.name} - {self.color} - {self.size}'
    
class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField()
    brand_id = models.AutoField(primary_key=True)
    def __str__(self):
        return self.name

class Customer (models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50)
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_delivered = models.DateTimeField(null=True, blank=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField('ShoeVariant', through='OrderItem', related_name='orders')

    def __str__(self):
        return f'Order {self.order_id} - {self.status}'

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')
    variant = models.ForeignKey('ShoeVariant', on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('order', 'variant')

    def __str__(self):
        return f'OrderItem - {self.variant} x {self.quantity}'

class Reviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
