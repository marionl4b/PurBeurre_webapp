import pytest

from website.models.product import Product
from website.models.product import Category


@pytest.mark.django_db
class TestModels:
    @pytest.fixture
    def setup(self):
        """ Init test data from models in test database """
        print("INIT DATA")

        # categories
        self.breakfast = Category.objects.create(name="breakfast")
        self.snacks = Category.objects.create(name="snacks")
        self.chocolate = Category.objects.create(name="chocolate")

        # products
        self.snicker = Product.objects.create(name="snicker", nutriscore="e")
        self.nutella = Product.objects.create(name="nutella", nutriscore="e")

        # pruduct-categories
        self.snicker.categories.add(self.snacks)
        self.nutella.categories.add(self.breakfast, self.chocolate)

    def test_product_has_category(self, setup):
        """ GIVEN : tests data for Category and Product
            THEN : retrieve category name for snickers product
            WHEN : many-to-many relation has been set between product and category """
        snicker_has_cat = self.snicker.categories.values("name")
        assert list(snicker_has_cat) == [{'name': 'snacks'}]

    def test_product_has_multiple_category(self, setup):
        nutella_categories = self.nutella.categories.values_list("name")
        assert list(nutella_categories) == [("breakfast",), ("chocolate",)]

    def test_raise_product_is_unique(self, setup):
        with pytest.raises(Exception):
            Product.objects.create(name="nutella", nutriscore="e")
