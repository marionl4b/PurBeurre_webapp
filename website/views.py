from django.shortcuts import render, get_object_or_404
from .models.product import Product


def home(request):
    return render(request, 'website/index.html')


def result(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'website/list_product.html', context)


def favorites(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'website/list_product.html', context)
