import pytest
from mixer.backend.django import mixer
from website.models import *
from django.contrib.auth.models import User


@pytest.fixture
def categories(db):
    print("INIT CATEGORIES")
    return (
        mixer.blend(Category, name="Petit-déjeuners"),
        mixer.blend(Category, name="Pâtes à tartiner"),
        mixer.blend(Category, name="Sodas"),
        mixer.blend(Category, name="Snacks")
    )


@pytest.fixture
def products(db):
    print("INIT PRODUCTS")
    return (
        mixer.blend(Product, name="Nutella", nutriscore="e"),
        mixer.blend(Product, name="Coca-Cola", nutriscore="e"),
        mixer.blend(Product, name="Snickers", nutrsiscore="e"),
        mixer.blend(Product, name="Coca-Cola zéro", nutrsicore="b")
    )


@pytest.fixture
def users(db):
    print("INIT USERS")
    return mixer.cycle(3).blend(User)


@pytest.mark.django_db
class TestModels:

    def test_created_categories(self, categories):
        assert Category.objects.count() == 4

    def test_created_products(self, products):
        assert Product.objects.count() == 4

    def test_created_users(self, users):
        assert User.objects.count() == 3

    def test_category_is_breackfast(self, categories):
        category_breakfast = Category.objects.get(name="Petit-déjeuners")
        assert category_breakfast.name == "Petit-déjeuners"

    def test_product_nutrsicore_is_e(self, products):
        nutella = Product.objects.get(name="Nutella")
        assert nutella.nutriscore == "e"
