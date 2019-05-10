import pytest
from django.contrib.auth.models import User

from website.models.product import Product
from website.models.product import Category


@pytest.mark.django_db
class TestModels:
    @pytest.fixture
    def setup(self):
        """ Init test data from models in test database
            tests data for Category, Product and User
            many-to-many relation has been set between Product and Category
            and Product and User (favorites)"""

        # categories
        self.breakfast = Category.objects.create(name="breakfast")
        self.snacks = Category.objects.create(name="snacks")
        self.chocolate = Category.objects.create(name="chocolate")

        # products
        self.snicker = Product.objects.create(name="snicker", nutriscore="e")
        self.nutella = Product.objects.create(name="nutella", nutriscore="e")

        # product-categories
        self.snicker.categories.add(self.snacks)
        self.nutella.categories.add(self.breakfast, self.chocolate)

        # authenticated user
        self.user = User.objects.create_user("username", "email@mailer.com", "password123")

        # product-favorites
        self.nutella.favorites.add(self.user)

    def test_product_has_category(self, setup):
        """retrieve category for snicker product"""
        snicker_has_cat = self.snicker.categories.values("name")
        assert list(snicker_has_cat) == [{'name': 'snacks'}]

    def test_product_has_multiple_category(self, setup):
        """retrieve categories for nutella product"""
        nutella_categories = self.nutella.categories.values_list("name")
        assert list(nutella_categories) == [("breakfast",), ("chocolate",)]

    def test_raise_product_is_unique(self, setup):
        """raise error when 2 product have the same name"""
        with pytest.raises(Exception):
            Product.objects.create(name="nutella", nutriscore="e")

    def test_user_has_favorite(self, setup):
        """retrieve same user id for product save as favorite by user 4"""
        user_fav = self.nutella.favorites.values("id")
        assert user_fav[0]["id"] == self.user.id
