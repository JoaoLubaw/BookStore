import json

from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from rest_framework.authtoken.models import Token

from django.urls import reverse

from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory
from product.models import Product

class TestProductViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        self.token = Token.objects.create(user=self.user)

        category = CategoryFactory()

        self.product = ProductFactory(
            title='pro controller',
            price=200.00,
            category=category.title
        )

        self.client.force_login(user=self.user)

    def test_get_all_product(self):
        response = self.client.get(
            reverse('product-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_data = json.loads(response.content)

        self.assertEqual(product_data[0]["title"], self.product.title)
        self.assertEqual(product_data[0]["price"], self.product.price)
        self.assertEqual(product_data[0]["active"], self.product.active)

    def test_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        category = CategoryFactory()
        data = json.dumps({
            'title': 'notebook',
            'price': 800.00,
            'category': [category.id for category in [category]]
        })

        response = self.client.post(
            reverse('product-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_product = Product.objects.get(title='notebook')

        self.assertEqual(created_product.title, 'notebook')
        self.assertEqual(created_product.price, 800.00)