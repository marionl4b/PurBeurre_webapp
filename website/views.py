from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm
from .models.product import Product


def home(request):
    return render(request, 'website/index.html')


def result(request):
    products = Product.objects.all()
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
            username = form.cleaned_data.get('username')
            messages.success(request, f"Compte créé pour {username}!")
            return redirect('register')
    else :
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'website/register.html', context)
