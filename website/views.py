from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import UserRegistrationForm
from .models.product import Product
from .models.category import Category
from .OFF_request import OFFRequest as OFFReq


def home(request):
    return render(request, 'website/index.html')


def legal(request):
    return render(request, 'website/legal.html')


def result(request):
    """ WHEN: search submit
        THEN: look in database for substitute
        in the same category of product and a lower nutriscore"""
    query = request.GET.get('q')  # retrieve user search query
    if query:
        try:
            # look for product matching query
            search_prod = Product.objects.get(name__icontains=query, nutriscore="e")
            # select the first category of the matching product
            search_cat = Category.objects.filter(product_category=search_prod.id)[:1]
            # return substitutes products in the same category with lower nutriscore
            products = Product.objects.filter(categories=search_cat).exclude(nutriscore="e")
        except ObjectDoesNotExist:
            OFFReq.request_constructor(OFFReq(), query)  # make OFF request when result not match
            products = Product.objects.all()  # return all products when result not match
    else:
        products = Product.objects.all()  # return all products when query is empty
    context = {'products': products}
    return render(request, 'website/list_product.html', context)


def detail(request, product_id):
    """ WHEN: product_id in database
        THEN: show product details and construct a dictionary for nutrients """
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    if product.nutrient_100g != "":
        nutrient_100g = sorted(product.nutrient_100g.split(","))
        nutrient_list = []
        if len(nutrient_100g) > 0:
            i = -1
            for n in nutrient_100g:
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


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             f"Votre compte vient d'être créé !, "
                             f"vous pouvez désormais vous connecter")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'website/register.html', context)


@login_required
def profile(request):
    return render(request, 'website/profile.html')
