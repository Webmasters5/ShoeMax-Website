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