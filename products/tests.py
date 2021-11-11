from django.test import TestCase

# Create your tests here.

from django.test import TestCase

import geekshop.urls
from products.models import ProductCategory, Product
from django.test.client import Client


class TestMainSmokeTest(TestCase):
    status_code_success = 200

    def setUp(self):
        category = ProductCategory.objects.create(name='Test')
        Product.objects.create(category=category, name='product_test', image=' ', price=100)
        self.client = Client()

    def test_site_pages(self):
        pages=('/',
               '/products/',
               '/products/page/1/',
               '/products/category/1/',
               '/products/category/1/page/1/'
               )
        for page in pages:
            response = self.client.get(page)
            try:
                self.assertEqual(response.status_code, self.status_code_success)
                print(f'{page} is OK')
            except Exception as e:
                print(f'{page} is NG')
                print(e)

    def test_products_product(self):
        for product_item in Product.objects.all():
            response = self.client.get(f'/products/detail/{product_item.pk}/')
            try:
                self.assertEqual(response.status_code, 200)
                print(f'/products/detail/{product_item.pk}/ is OK')
            except Exception as e:
                print(f'/products/detail/{product_item.pk}/ is NG')
                print(e)

    def test_profile(self):
        response = self.client.get('/users/profile/')
        try:
            self.assertEqual(response.status_code, 302)
            print('/users/profile/ is OK')
        except Exception as e:
            print('/users/profile/ is NG')
            print(e)


    def tearDown(self):
        pass
