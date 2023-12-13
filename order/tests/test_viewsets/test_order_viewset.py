import json

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory, OrderFactory
from product.models import Product
from order.models import Order

class TestOrderViewSet(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory(title='technology')
        self.product = ProductFactory(title='mouse', price=100, category=[self.category])

    def test_order(self):
        order = OrderFactory(product=[self.product])

        response = self.client.get(
            reverse('order-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data_list = json.loads(response.content)

        # Verifique se a lista não está vazia antes de acessar os índices
        self.assertTrue(order_data_list)

        # Agora, se houver pedidos, pegue o primeiro
        if order_data_list:
            first_order = order_data_list[0]

            # Verifique se o produto na ordem tem uma categoria antes de acessar os índices
            self.assertTrue(first_order['product'])

            # Agora, se houver um produto, pegue o primeiro
            first_product = first_order['product'][0]

            # Verifique se o produto tem uma categoria antes de acessar os índices
            self.assertTrue(first_product['category'])

            # Agora, se houver uma categoria, pegue a primeira
            first_category = first_product['category'][0]

            # Finalmente, verifique se o título da categoria corresponde ao esperado
            self.assertEqual(first_category, self.category.id)
    def test_create_order(self):
        data = json.dumps({
            'product': [{'id': self.product.id, 'title': 'Mouse', 'category': [self.category.id]}],
            'products_id': [self.product.id],
            'user': self.user.id
        })

        response = self.client.post(
            reverse('order-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=self.user)

        self.assertEqual(created_order.user, self.user)
        self.assertEqual(created_order.product.first(), self.product)
