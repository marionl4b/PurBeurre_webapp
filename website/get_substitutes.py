import requests
from PurBeurre_webapp.settings import URL_PRODUCT, URL_SUBSTITUTE
from .models.product import Product
from .models.category import Category


class Substitutes:
    """ Select Substitutes for user search in database fisrt and then
        Retreive data from Open Food Fact API (OFF) and parse them for database insertion"""

    def __init__(self):
        self.url_product = URL_PRODUCT
        self.url_substitute = URL_SUBSTITUTE

    def select_substitutes(self, query):
        """ Select substitutes matching result in database"""
        if Product.objects.filter(name__icontains=query):
            selection = Product.objects.filter(name__icontains=query).first()
            search_prod = Product.objects.get(name=selection)
            # store the nutriscore of the searched product
            search_nutriscore = search_prod.nutriscore
            # select the first category of the matching product
            search_cat = Category.objects.filter(product_category=search_prod.id)[:1]
            # return substitutes products in the same category with lower nutriscore
            substitutes = Product.objects.filter(categories=search_cat,
                                                 nutriscore__lt=search_nutriscore)
            results = (search_prod, substitutes)
            return results

    def api_request(self, search_term, search_type):
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

    def prod_parser(self, response):
        """parse OFF json response in a dictionary of searched product and substitutes
        for Product model database insertion"""
        products = []
        i = 0
        for product in response:
            # crawling product for name, desc, API_url, image_url, nutriscore, nutient_100g
            if 'ingredients_text_fr' not in product:
                desc = ""
            else:
                desc = product['ingredients_text_fr']
            nutrigrade = "".join(product["nutrition_grades_tags"])
            if nutrigrade in ("a", "b", "c", "d", "e") \
                    and 'fat_100g' in product['nutriments'] \
                    and 'image_url' in product \
                    and 'product_name_fr' in product:
                i += 1
                product[i] = {
                    "name": product['product_name_fr'],
                    "desc": desc,
                    "categories": product["categories"].split(","),
                    "API_link": product['url'],
                    "photo": product['image_url'],
                    "nutriscore": nutrigrade,
                    "nutrient_100g":
                        "saturated_fat_100g:{}:{}, ".format(
                        product['nutriments']['saturated-fat_100g'],
                        product['nutrient_levels']['saturated-fat']) +
                        "fat_100g:{}:{}, ".format(
                        product['nutriments']['fat_100g'], product['nutrient_levels']['fat']) +
                        "salt_100g:{}:{}, ".format(
                        product['nutriments']['salt_100g'], product['nutrient_levels']['salt']) +
                        "sugars_100g:{}:{} ".format(
                        product['nutriments']['sugars_100g'], product['nutrient_levels']['sugars'])
                }
                products.append(product[i])
            else:
                pass
        return products

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
                                                               photo=product["photo"],
                                                               API_link=product["API_link"],
                                                               nutriscore=product["nutriscore"],
                                                               nutrient_100g=product["nutrient_100g"],
                                                               )

                    Product.objects.get(name=product["name"]).categories.add(category.id)
        else:
            return None

    def run(self, search_term):
        """run parser and crawl OFF data to construct a dump of searched product,
        categories and substitutes products. Then serialize and insert this data to database """
        response = self.api_request(search_term, "product")
        products = self.prod_parser(response)
        response = self.api_request(products[0]["categories"][0], "substitute")
        substitutes = self.prod_parser(response)
        search_prod = products[0]
        substitutes.append(search_prod)
        data = {"substitutes": substitutes}
        self.insert_data(data)
