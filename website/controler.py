from .models import Product
from .models import Category


class Controler:
    def __init__(self):
        pass

    def get_substitutes(self, query):
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

    def show_product_detail(self):
        pass

    def nutrient_parser(self):
        pass
