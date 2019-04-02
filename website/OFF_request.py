import requests
import json


class OFFRequest:
    """Retreive data from Open Food Fact API (OFF) and parse them for database insertion"""

    def __init__(self):
        self.url_product = 'https://fr.openfoodfacts.org/cgi/search.pl?search_terms={}' \
                   '&search_simple=1&action=process&nutrition_grades=e' \
                   '&sort_by=unique_scans_n&page=1&json=1'
        self.url_substitute = "https://fr.openfoodfacts.org/cgi/search.pl?action=process" \
                              "&tagtype_0=categories&tag_contains_0=contains&tag_0={}" \
                              "&tagtype_1=nutrition_grades&tag_contains_1=does_not_contain" \
                              "&tag_1=E&sort_by=unique_scans_n&page_size=20&json=1"

    def API_request(self, search_term, search_type):
        """request OFF in json"""
        url = ""
        if search_type == "categories":
            url = self.url_product.format(search_term)
        elif search_type == "products":
            url = self.url_substitute.format(search_term)
        r = requests.get(url)
        response = r.json()
        return response["products"]

    def cat_parser(self, response):
        """parse OFF json response in a dictionary for categories database insertion
        and substitute request"""
        categories = []
        for product in response:
            # crawling categories of each product
            prod_cat = product["categories"].split(",")
            for cat in prod_cat:
                if cat not in categories:
                    categories.append(cat)
        return categories

    def sub_parser(self, response):
        """parse OFF json response in a dictionary for product database insertion"""
        products = []
        i = 0
        for product in response:
            # crawling product for name, desc, API_url, image_url, nutriscore, nutient_100g
            nutrigrade = "".join(product["nutrition_grades_tags"])
            if nutrigrade in ("a", "b", "c", "d"):
                i += 1
                product[i] = {
                    "name": product['product_name_fr'],
                    "desc": product['ingredients_text_fr'],
                    "categories": product["categories"].split(","),
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
        return products

    def dump_data(self, data):
        """json dump of data"""
        with open('website/OFF_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def insert_data(self):
        """insert data of OFF_data.json in database for Category and Product"""
        pass

    def run(self, search_term):
        response = self.API_request(search_term, "categories")
        categories = self.cat_parser(response)
        response = self.API_request(categories[-1], "products")
        products = self.sub_parser(response)
        data = {
            "categories": categories,
            "products": products
        }
        self.dump_data(data)
