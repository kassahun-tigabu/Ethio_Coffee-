from django.db import models
from django.conf import settings
from products.models import CoffeeProduct

ORDER_STATUS = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
]

PAYMENT_METHODS = [
    ('telebirr', 'Telebirr'),
    ('cbe_birr', 'CBE Birr'),
    ('bank_transfer', 'Bank Transfer'),
    ('cash_on_delivery', 'Cash on Delivery'),
]

class Order(models.Model):
    order_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Shipping information
    shipping_name = models.CharField(max_length=100)
    shipping_phone = models.CharField(max_length=15)
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=50)
    shipping_region = models.CharField(max_length=50)
    
    # Order details
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed')],
        default='pending'
    )
    
    # Order status
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.order_number
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import datetime
            self.order_number = f"ETH-{datetime.datetime.now().strftime('%Y%m%d')}-{Order.objects.count() + 1:04d}"
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(CoffeeProduct, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=200)  # Store product name at time of order
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Store price at time of order
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product_name}"
    
    def save(self, *args, **kwargs):
        self.total = self.price * self.quantity
        super().save(*args, **kwargs)