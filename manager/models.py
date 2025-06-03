from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Stock(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_level = models.IntegerField(default=5)  # 🔸 NEW FIELD

    def __str__(self):
        return self.name

class Sale(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sold {self.quantity_sold} of {self.stock.name} on {self.date.date()}"

    def profit(self):
        return (self.sale_price - self.stock.price) * self.quantity_sold

