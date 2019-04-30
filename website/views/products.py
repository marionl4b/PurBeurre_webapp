from django.contrib import auth
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from website.models.product import Product
from website.get_substitutes import Substitutes as Sub


def result(request):
    """ WHEN: search submit
        THEN: look in database for substitute
        in the same category of product and a lower nutriscore"""
    query = request.GET.get('q')  # retrieve user search query
    results = Sub.select_substitutes(Sub(), query)  # try to select in database matching result
    if not results:
        Sub.run(Sub(), query)  # run OFF request parser and insert if not in database
        results = Sub.select_substitutes(Sub(), query)  # try to select in database matching result
        if not results:
            context = {}  # None display error message
        else:
            context = {'search_prod': results[0], 'products': results[1]}
    else:
        context = {'search_prod': results[0], 'products': results[1]}
    return render(request, 'website/list_product.html', context)


def detail(request, product_id):
    """ WHEN: product_id in database
        THEN: show product details and construct a dictionary for nutrients """
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    if product.nutrient_100g is not None:
        nutrient_100g = sorted(product.nutrient_100g.split(","))
        nutrient_list = []
        if len(nutrient_100g) > 0:
            i = -1
            for item in nutrient_100g:
                i += 1
                n = nutrient_100g[i].split(":")
                nutrient_list.append(n)
            nutrients = {
                'fat': nutrient_list[0][1],
                'saturated_fat': nutrient_list[1][1],
                'sugars': nutrient_list[2][1],
                'salt': nutrient_list[3][1],
                'fat_level': nutrient_list[0][2],
                'saturated_fat_level': nutrient_list[1][2],
                'sugars_level': nutrient_list[2][2],
                'salt_level': nutrient_list[3][2],
            }
            context = {'product': product, 'nutrients': nutrients}
    return render(request, 'website/detail_product.html', context)


@login_required
def favorites(request):
    """ GIVEN: user loged
        WHEN: favorite submit
        THEN: add an association user/product in database
        and return user favorites product list"""
    user = auth.get_user(request)
    if user:
        if request.method == 'POST':
            product_id = request.POST.get('fav')
            Product.objects.get(id=product_id).favorites.add(user.id)
        context = {"products": Product.objects.filter(favorites=user.id),
                   "favorites": user.favorite.all()}
        return render(request, 'website/list_product.html', context)
    else:
        return redirect('login')
