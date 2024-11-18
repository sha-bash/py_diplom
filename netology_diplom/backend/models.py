from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Shop(models.Model):
    name = models.CharField(max_length=50, unique=True)
    url = models.URLField(unique=True)
    user = models.OneToOneField(User, verbose_name='User',
                               blank=True, null=True,
                               on_delete=models.CASCADE)
    state = models.BooleanField(verbose_name='Shop status', default=True)

    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = "Shops"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)
    shops = models.ManyToManyField(Shop, verbose_name='Shops', related_name='categories', blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = "Categories"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=80, unique=True)
    category = models.ForeignKey(Category, verbose_name='Category',
                                related_name='products', blank=True,
                                on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = "Products"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, verbose_name='Product',
                               related_name='product_infos',
                               blank=True,
                               on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name='Shop',
                            related_name='product_infos',
                            blank=True,
                            on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    quantity = models.PositiveIntegerField(verbose_name='Quantity')
    price = models.DecimalField(max_digits=20, decimal_places=2,
                              verbose_name='Price',
                              validators=[MinValueValidator(0)])
    price_rrc = models.DecimalField(max_digits=20, decimal_places=2,
                                   verbose_name='Recommended retail price',
                                   validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Product information'
        verbose_name_plural = "Product information"
        constraints = [
            models.UniqueConstraint(fields=['product', 'shop'], name='unique_product_shop'),
        ]

    def __str__(self):
        return f"{self.shop.name} - {self.product.name}"


class Parameter(models.Model):
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        verbose_name = 'Parameter'
        verbose_name_plural = "Parameters"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, verbose_name='Product information',
                                   related_name='product_parameters',
                                   blank=True,
                                   on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, verbose_name='Parameter',
                                related_name='product_parameters',
                                blank=True,
                                on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Value', max_length=100)

    class Meta:
        verbose_name = 'Product parameter'
        verbose_name_plural = "Product parameters"
        constraints = [
            models.UniqueConstraint(fields=['product_info', 'parameter'], name='unique_product_parameter'),
        ]

    def __str__(self):
        return f"{self.product_info.product.name} - {self.parameter.name}"


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='User',
                            related_name='orders',
                            blank=True,
                            on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    state = models.CharField(verbose_name='Status', max_length=15)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = "Orders"
        ordering = ('-dt',)

    def __str__(self):
        return str(self.dt)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Order',
                             related_name='ordered_items',
                             blank=True,
                             on_delete=models.CASCADE)
    product_info = models.ForeignKey(ProductInfo, verbose_name='Product information',
                                   related_name='ordered_items',
                                   blank=True,
                                   on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Quantity')

    class Meta:
        verbose_name = 'Order item'
        verbose_name_plural = "Order items"
        constraints = [
            models.UniqueConstraint(fields=['order', 'product_info'], name='unique_order_item'),
        ]

    def __str__(self):
        return str(self.order.dt)


class Contact(models.Model):
    user = models.ForeignKey(User, verbose_name='User',
                            related_name='contacts',
                            blank=True,
                            on_delete=models.CASCADE)
    city = models.CharField(max_length=50, verbose_name='City')
    street = models.CharField(max_length=100, verbose_name='Street')
    house = models.CharField(max_length=15, verbose_name='House', blank=True)
    structure = models.CharField(max_length=15, verbose_name='Structure', blank=True)
    building = models.CharField(max_length=15, verbose_name='Building', blank=True)
    apartment = models.CharField(max_length=15, verbose_name='Apartment', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Phone')

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = "Contacts"

    def __str__(self):
        return f"{self.city} {self.street} {self.house}"
