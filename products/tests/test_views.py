from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase, APIClient

from accounts.models import User
from products.models import Product, Category


class TestProduct(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test category', properties={'color': 'string'})
        self.product = Product.objects.create(
            name='test product',
            price=10,
            properties={'color': 'string'},
        )
        self.product.categories.add(self.category)
        self.user = User.objects.create_superuser(phone_number=9300085358, password='test')
        self.test_client = APIClient()

    def test_api_categories(self):
        category_url = api_reverse('categories-list')
        category_r = self.test_client.get(path=category_url)
        self.assertEqual(category_r.status_code, status.HTTP_200_OK)
        self.assertContains(category_r, 'test category', status_code=status.HTTP_200_OK)
        self.assertEqual(category_r.json().get('count'), 1)

    def test_api_bookmark(self):
        token_url = api_reverse('obtain-token')
        bookmark_url = api_reverse('products-bookmark', kwargs={'pk': self.product.id})
        obtain_r = self.test_client.post(
            path=token_url,
            data={'phone_number': 9300085358, 'password': 'test'}
        )
        jwt_token = obtain_r.json().get('access')
        self.test_client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')
        bookmark_r = self.test_client.post(path=bookmark_url, data={'like_status': True})
        self.assertContains(bookmark_r, 'true', status_code=status.HTTP_201_CREATED)

    def test_api_register(self):
        register_url = api_reverse('register')
        register_r = object
        for num in range(10):
            register_r = self.test_client.post(path=register_url, data={})
        self.assertEqual(register_r.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
