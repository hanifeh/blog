from django.test import TestCase

# Create your tests here.
from . import enums
from .models import Product


class ProductTestCase(TestCase):
    """
    Tests for Product model
    """

    def setUp(self):
        """
        Set up the test requirements
        """

        Product.objects.create(
            name='Test PROD1',
            description='Test PROD1 Desc',
            qty_in_stock=100,
            is_active=True,
            type=enums.ProductTypes.PRINT
        )

    def test_deduct_from_stock(self):
        """
        Tests deduct_from_stock model method
        """
        obj = Product.objects.first()
        qty = obj.deduct_from_stock(10)
        self.assertEqual(qty, 90)
