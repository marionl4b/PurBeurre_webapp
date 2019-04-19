import pytest

from website import OFF_request
from .test_models import Product, Category


@pytest.mark.django_db
class TestOffRequest:
    @pytest.fixture
    def setup(self, client):
        self.offreq_dump_ok = [{
                "product_name_fr": "Coca Cola Light",
                "image_url": "https://static.openfoodfacts.org/images/products/544/900/005/0205/front_fr.59.400.jpg",
                "categories": "Boissons, Boissons édulcorées, Boissons gazeuses, Boissons light, Sodas, Sodas light, Sodas au cola, Sodas au cola light",
                # "ingredients_text": "Eau gazéifiée, colorant : caramel (E150d), acidifiants (acide phosphorique, acide citrique), édulcorants (aspartame, acesulfame K), extraits végétaux, arôme caféine",
                "nutrition_grades_tags": [ "b", ],
                "nutriments": {
                    "fat_100g": "0",
                    "salt_100g": 0.07,
                    "sugars_100g": "0",
                    "saturated-fat_100g": "0", },
                "nutrient_levels": {
                    "saturated-fat": "low",
                    "fat": "low",
                    "salt": "low",
                    "sugars": "low"},
                "url": "https://fr.openfoodfacts.org/produit/5449000053565/coca-cola-light", }, ]
        self.offreq_dump_fail = [{
                "product_name": "Coca Cola Zéro",
                "ingredients_text_fr": "Eau gazéifiée ; colorant : E150d ; acidifiants : acide phosphorique, citrate de sodium ; \r\nédulcorants : aspartame, acésulfame-K ; arômes naturels (extraits végétaux), dont caféine. \r\nContient une source de phénylalanine.",
                "image_url": "https://static.openfoodfacts.org/images/products/500/011/260/9516/front_fr.42.400.jpg",
                "nutriments": {
                    "saturated-fat_100g": "0",
                    "sugars_100g": "0",
                    "salt_100g": 0.02,
                    "fat_100g": "0", },
                "nutrition_grades_tags": ["b"],
                "url": "https://fr.openfoodfacts.org/produit/5000112609516/coca-cola-zero",

                "nutrient_levels": {
                    "fat": "low",
                    "saturated-fat": "low",
                    "salt": "low",
                    "sugars": "low"}, }, ]
        self.parser_results = [{
            "name": "Coca Cola Light",
            "desc": "",
            "categories": ["Boissons", "Boissons édulcorées", "Boissons gazeuses", "Boissons light",
                           "Sodas", "Sodas light", "Sodas au cola", "Sodas au cola light"],
            "API_link": "https://fr.openfoodfacts.org/produit/5449000053565/coca-cola-light",
            "photo": "https://static.openfoodfacts.org/images/products/544/900/005/0205/front_fr.59.400.jpg",
            "nutriscore": "b",
            "nutrient_100g": "saturated_fat_100g:0:low, fat_100g:0:low, salt_100g:0.07:low, sugars_100g:0:low "
        },]

    def test_parser_success(self, setup):
        result = OFF_request.OFFRequest.prod_parser(OFF_request.OFFRequest(), self.offreq_dump_ok)
        assert result == self.parser_results

    def test_parser_fail(self, setup):
        result = OFF_request.OFFRequest.prod_parser(OFF_request.OFFRequest(), self.offreq_dump_fail)
        assert len(result) == 0
