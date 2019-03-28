from django.shortcuts import render, get_object_or_404
from .models.product import Product


def home(request):
    return render(request, 'website/index.html')


def result(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'website/list_product.html', context)


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'website/detail_product.html', context)
