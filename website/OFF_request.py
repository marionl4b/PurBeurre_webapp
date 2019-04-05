import requests
import json
from .models.product import Product
from .models.category import Category


class OFFRequest:
    """Retreive data from Open Food Fact API (OFF) and parse them for database insertion"""

    def __init__(self):
        self.url_product = 'https://fr.openfoodfacts.org/cgi/search.pl?search_terms={}' \
                   '&search_simple=1&action=process&nutrition_grades=e' \
                   '&sort_by=unique_scans_n&page=1&json=1'
        self.url_substitute = "https://fr.openfoodfacts.org/cgi/search.pl?action=process&" \
                              "tagtype_0=countries&tag_contains_0=contains&tag_0=france" \
                              "&tagtype_1=nutrition_grades&tag_contains_1=does_not_contain&tag_1=E%2C%20D" \
                              "&sort_by=unique_scans_n&page=1&search_terms={}&json=1"

    def API_request(self, search_term, search_type):
        """request OFF with product term for categories search type
        and request OFF with category term restric by nutriscore non containing 'e'
        for product search type"""
        url = ""
        if search_type == "product":
            url = self.url_product.format(search_term)
        elif search_type == "substitute":
            url = self.url_substitute.format(search_term)
        r = requests.get(url)
        response = r.json()
        return response["products"]

    def cat_parser(self, response):
        """parse OFF json response in a dictionary for Categories model database insertion
        and substitute request"""
        categories = []
        for product in response:
            # crawling categories of each product
            prod_cat = product["categories"].split(", ")
            for cat in prod_cat:
                if cat not in categories:
                    categories.append(cat)
        return categories

    def prod_parser(self, response):
        """parse OFF json response in a dictionary of searched product and substitutes
        for Product model database insertion"""
        products = []
        i = 0
        for product in response:
            # crawling product for name, desc, API_url, image_url, nutriscore, nutient_100g
            nutrigrade = "".join(product["nutrition_grades_tags"])
            if nutrigrade in ("a", "b", "c", "d", "e"):
                i += 1
                product[i] = {
                    "name": product['product_name_fr'],
                    "desc": product['ingredients_text_fr'],
                    "categories": product["categories"].split(", "),
                    "API_url": product['url'],
                    "image_url": product['image_url'],
                    "nutriscore": nutrigrade,
                    "nutrient_100g": "saturated_fat_100g:{}:{}, ".format(
                        product['nutriments']['saturated-fat_100g'],
                        product['nutrient_levels']['saturated-fat']) + "fat_100g:{}:{}, ".format(
                        product['nutriments']['fat_100g'],
                        product['nutrient_levels']['fat']) + "salt_100g:{}:{}, ".format(
                        product['nutriments']['salt_100g'],
                        product['nutrient_levels']['salt']) + "sugars_100g:{}:{} ".format(
                        product['nutriments']['sugars_100g'], product['nutrient_levels']['sugars'])
                }
                products.append(product[i])
            else:
                pass
        return products

    def dump_data(self, data):
        """json dump of data"""
        with open('website/OFF_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def insert_data(self, data):
        """insert data of OFF_data.json in database for Category and Product"""
        category_name = data["substitutes"][0]["categories"][0]
        products = data["substitutes"]
        if len(products) != 0:
            i = 0
            Category.objects.get_or_create(name=category_name)
            category = Category.objects.get(name=category_name)
            for product in products:
                i += 1
                if Product.objects.filter(name=product["name"]).exists():
                    pass
                else:
                    product[i] = Product.objects.get_or_create(name=product["name"],
                                                               desc=product["desc"],
                                                               photo=product["image_url"],
                                                               API_link=product["API_url"],
                                                               nutriscore=product["nutriscore"],
                                                               nutrient_100g=product["nutrient_100g"],
                                                               )

                    Product.objects.get(name=product["name"]).categories.add(category.id)

    def run(self, search_term):
        """run parser and crawl OFF data to construct a dump of searched product,
        categories and substitutes products. Then serialize and insert this data to database """
        response = self.API_request(search_term, "product")
        # categories = self.cat_parser(response)
        products = self.prod_parser(response)
        response = self.API_request(products[0]["categories"][0], "substitute")
        substitutes = self.prod_parser(response)
        product = products[0]
        substitutes.append(product)
        data = {
            # "categories": categories,
            "substitutes": substitutes
        }
        self.dump_data(data)
        self.insert_data(data)
