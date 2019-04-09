from .models import Product
from .models import Category
from .OFF_request import OFFRequest as OFFReq


class Controler:
    def __init__(self):
        pass

    def check_in_database(self, query):
        # look for product matching query
        if Product.objects.filter(name__icontains=query):
            return self.run_substitutes_selection(query)
        else:
            return OFFReq.run(OFFReq(), query)  # make OFF request when result not match

    def run_substitutes_selection(self, query):
        # look for product matching query
        selection = Product.objects.filter(name__icontains=query).first()
        search_prod = Product.objects.get(name=selection)
        # store the nutriscore of the searched product
        search_nutriscore = search_prod.nutriscore
        # select the first category of the matching product
        search_cat = Category.objects.filter(product_category=search_prod.id)[:1]
        # return substitutes products in the same category with lower nutriscore
        substitutes = Product.objects.filter(categories=search_cat, nutriscore__lt=search_nutriscore)
        return search_prod, substitutes

    def show_product_detail(self):
        pass

    def nutrient_parser(self):
        pass
