from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count

# Create your models here.

class Category(models.Model):
    category_name       = models.CharField(max_length=50, unique=True)
    slug                = models.SlugField(max_length=100, unique=True)
    description         = models.TextField(max_length=255, blank=True)
    Cat_image           = models.ImageField(upload_to='static/images', blank=True)

    class Meta:
        verbose_name        =   'category'
        verbose_name_plural =   'categories'

    def __str__(self):
        return self.category_name

class Dishes_model(models.Model):
    dish_name           = models.CharField(max_length=200, unique=True, null=True, blank=True)
    slug                = models.SlugField(max_length=100, null=True, blank=True)
    description         = models.TextField(max_length=200, null=True, blank=True)
    category            = models.ForeignKey(Category, on_delete=models.CASCADE)
    ingredients         = models.TextField(max_length=200, null=True, blank=True)
    image               = models.ImageField(upload_to="static/images")
    is_available        = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        =   'Dish'
        verbose_name_plural =   'Dishes'

    def averagereview(self):
        reviews = ReviewRating.objects.filter(dish=self,status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countreview(self):
        reviews = ReviewRating.objects.filter(dish=self,status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    
    def __str__(self):
        return f"{self.id}) {self.dish_name}"

# variation manager and model
class VariationManager(models.Manager):
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size',is_active=True)

variation_category_choice = (
    ('size','size'),
)

class Variation(models.Model):
    dish                = models.ForeignKey(Dishes_model, on_delete=models.CASCADE)
    variation_category  = models.CharField(max_length=50, choices = variation_category_choice )
    variation_value     = models.CharField(max_length=50)
    price               = models.IntegerField(null=True, blank=True)
    stock               = models.IntegerField(null=True, blank=True)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


# review and rating of the dish
class ReviewRating(models.Model):
    dish                = models.ForeignKey(Dishes_model, on_delete=models.CASCADE)
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    subject             = models.CharField(max_length=100, blank = True)
    review              = models.TextField(max_length = 500, blank = True)
    rating              = models.FloatField(null=True, blank = True)
    status              = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now_add=True)
    updated_date         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


# photos of dishes
class Dish_gallery(models.Model):
    dish                = models.ForeignKey(Dishes_model, on_delete=models.CASCADE)
    image               = models.ImageField(upload_to="static/images")
    created_date        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dish.dish_name




class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )

    user = models.ForeignKey(User,on_delete=models.SET_NULL, null = True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True ,null = True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50, blank = True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=50,blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS, default = 'New')
    ip = models.CharField(max_length=50)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null = True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True ,null = True)
    dish = models.ForeignKey(Dishes_model,on_delete=models.CASCADE)
    variations  = models.ManyToManyField(Variation, blank = True)
    quantity = models.IntegerField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name