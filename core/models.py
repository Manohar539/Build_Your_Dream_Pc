from django.db import models
from django.contrib.auth.models import User


class Component(models.Model):

    CATEGORY_CHOICES = [
        ('cpu', 'CPU'),
        ('gpu', 'GPU'),
        ('ram', 'RAM'),
        ('storage', 'Storage'),
        ('motherboard', 'Motherboard'),
        ('psu', 'PSU'),
        ('case', 'Case'),
        ('cooling', 'Cooling')
    ]

    USECASE_CHOICES = [
        ('gaming', 'Gaming'),
        ('students', 'Students'),
        ('it', 'IT'),
        ('creators', 'Creators')
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    use_case = models.CharField(max_length=20, choices=USECASE_CHOICES)

    price = models.FloatField()

    socket_type = models.CharField(max_length=50, blank=True)
    ram_variant = models.CharField(max_length=50, blank=True)

    power_draw = models.IntegerField(default=0)

    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.title


class Build(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    cpu = models.CharField(max_length=200, blank=True)
    gpu = models.CharField(max_length=200, blank=True)
    ram = models.CharField(max_length=200, blank=True)

    motherboard = models.CharField(max_length=200, blank=True)
    storage = models.CharField(max_length=200, blank=True)

    psu = models.CharField(max_length=200, blank=True)
    case = models.CharField(max_length=200, blank=True)
    cooling = models.CharField(max_length=200, blank=True)

    total_price = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Build {self.id} - {self.owner.username}"


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    cpu = models.CharField(max_length=200, blank=True)
    gpu = models.CharField(max_length=200, blank=True)
    ram = models.CharField(max_length=200, blank=True)

    motherboard = models.CharField(max_length=200, blank=True)
    storage = models.CharField(max_length=200, blank=True)

    psu = models.CharField(max_length=200, blank=True)
    case = models.CharField(max_length=200, blank=True)
    cooling = models.CharField(max_length=200, blank=True)

    total_price = models.FloatField(default=0)

    customer_name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    payment_method = models.CharField(max_length=50)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    profit = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username