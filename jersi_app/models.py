from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Jersi(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='jerseys', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    detail = models.CharField(max_length=500)
    quantity = models.PositiveIntegerField(default=1)
  
    image = models.ImageField(upload_to='jersi_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jersi = models.ForeignKey(Jersi, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.jersi.name}"
    
    
    


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    order_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.address_line_1}, {self.city}, {self.state}, {self.country}"