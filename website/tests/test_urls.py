from django.urls import resolve, reverse
import pytest
from .test_models import Product


@pytest.mark.django_db
class TestUrls:
    @pytest.fixture
    def setup(self):
        """ Init test data from models in test database """
        print("INIT DATA")

        self.nutella = Product.objects.create(name="nutella", nutriscore="e")

    def test_home(self):
        """test homepage"""
        path = reverse('home')
        assert resolve(path).view_name == 'home'

    def test_search_result(self):
        """test search result page"""
        path = reverse('website:result')
        assert resolve(path).view_name == 'website:result'

    def test_search_product_detail(self, setup):
        """test product detail page for nutella"""
        product_id = self.nutella.id
        path = reverse('website:detail', args=(product_id,))
        assert resolve(path).view_name == 'website:detail'
