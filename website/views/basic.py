from django.contrib import messages, auth
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from website.forms import UserRegistrationForm
from website.models.product import Product
from website.get_substitutes import Substitutes as Sub


def home(request):
    return render(request, 'website/index.html')


def legal(request):
    return render(request, 'website/legal.html')

