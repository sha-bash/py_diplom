import logging
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Shop, Category, Product, Order, OrderItem, ProductInfo

User = get_user_model()

# Настройка логгера
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ShopTests(TestCase):
    def setUp(self):
        logger.info("Настройка тестов покупок")
        self.shop = Shop.objects.create(
            name="Test Shop",
            url="http://testshop.com"
        )

    def tearDown(self):
        logger.info("Прерывание тестов покупок")

    def test_shop_creation(self):
        logger.info("Создание тестового магазина")
        self.assertEqual(self.shop.name, "Test Shop")
        self.assertEqual(self.shop.url, "http://testshop.com")

class CategoryTests(TestCase):
    def setUp(self):
        logger.info("Настройка тестов категорий")
        self.category = Category.objects.create(
            name="Test Category"
        )

    def tearDown(self):
        logger.info("Прерывание тестов категорий")

    def test_category_creation(self):
        logger.info("Тестирование создания категорий")
        self.assertEqual(self.category.name, "Test Category")

class ProductTests(TestCase):
    def setUp(self):
        logger.info("Настройка тестов товаров")
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category
        )

    def tearDown(self):
        logger.info("Прерывание тестов товаров")

    def test_product_creation(self):
        logger.info("Тестирование создания товаров")
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.category, self.category)

class CartAPITests(APITestCase):
    def setUp(self):
        logger.info("Настройка API тестов корзины")
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
            price=100
        )
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        logger.info("Прерывание API тестов корзины")

    def test_add_to_cart(self):
        logger.info("Тестирование добавления в корзину")
        url = reverse('cart-list')
        data = {
            'product': self.product.id,
            'quantity': 2
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderItem.objects.count(), 1)
        logger.info("Товар добавлен в корзину: %s", response.data)

    def test_remove_from_cart(self):
        logger.info("Тестирование удаления из корзины")
        # Сначала добавляем товар в корзину
        order = Order.objects.create(user=self.user, state='cart')
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            price=self.product.price
        )
        
        url = reverse('cart-detail', args=[order_item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OrderItem.objects.count(), 0)
        logger.info("Товар удален из корзины: %s", order_item)

    def test_view_cart(self):
        logger.info("Тестирование просмотра корзины")
        url = reverse('cart-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        logger.info("Корзина просмотрена: %s", response.data)

class OrderAPITests(APITestCase):
    def setUp(self):
        logger.info("Настройка тестов OrderAPITests")
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
            price=100
        )
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        logger.info("Прерывание OrderAPITests")

    def test_create_order(self):
        logger.info("Тестирование создания заказа")
        # Сначала добавляем товар в корзину
        cart_order = Order.objects.create(user=self.user, state='cart')
        OrderItem.objects.create(
            order=cart_order,
            product=self.product,
            quantity=1,
            price=self.product.price
        )

        url = reverse('order-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.filter(state='new').count(), 1)
        logger.info("Заказ создан: %s", response.data)

    def test_create_empty_order(self):
        logger.info("Тестирование создания пустого заказа")
        url = reverse('order-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        logger.info("Создание пустого заказа не удалось: %s", response.data)

    def test_view_orders(self):
        logger.info("Тестирование просмотра заказов")
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        logger.info("Заказы просмотрены: %s", response.data)

class AuthenticationTests(APITestCase):
    def setUp(self):
        logger.info("Настройка тестов аутентификации")
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com'
        }

    def tearDown(self):
        logger.info("Прерывание тестов аутентификации")

    def test_user_registration(self):
        logger.info("Тестирование регистрации пользователя")
        url = reverse('user-register')
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        logger.info("Пользователь зарегистрирован: %s", response.data)

    def test_user_login(self):
        logger.info("Тестирование входа пользователя")
        # Сначала создаем пользователя
        User.objects.create_user(**self.user_data)
        
        url = reverse('user-login')
        response = self.client.post(url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        logger.info("Пользователь вошел в систему: %s", response.data)

class ProductInfoTests(TestCase):
    def setUp(self):
        logger.info("Настройка тестов ProductInfoTests")
        self.shop = Shop.objects.create(name="Test Shop", url="http://testshop.com")
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(name="Test Product", category=self.category)
        self.product_info = ProductInfo.objects.create(
            product=self.product,
            shop=self.shop,
            quantity=10,
            price=100,
            price_rrc=120
        )

    def tearDown(self):
        logger.info("Прерывание тестов ProductInfoTests")

    def test_product_info_creation(self):
        logger.info("Тестирование создания информации о товаре")
        self.assertEqual(self.product_info.product, self.product)
        self.assertEqual(self.product_info.shop, self.shop)
        self.assertEqual(self.product_info.quantity, 10)
        self.assertEqual(self.product_info.price, 100)
        self.assertEqual(self.product_info.price_rrc, 120)