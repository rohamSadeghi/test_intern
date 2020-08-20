from django.shortcuts import render, get_object_or_404

from products.forms import ProductForm
from products.models import Product, Store


def home(request):
    return render(request, 'base.html')

def product_detail_view(request, pk):
    # product_obj = Product.objects.get(pk=pk)
    product_obj = get_object_or_404(Product, pk=pk)
    try:
        product_obj = Product.objects.get(pk=pk)
    except Product.MultipleObjectsReturned:
        raise


    context = {'obj': product_obj}

    return render(request, 'products/product_detail.html', context=context)


def products_list(request):
    queryset = Product.objects.all()

    context = {'products': queryset}

    return render(request, 'products/products_list.html', context)

def stores_list(request):
    queryset = Store.objects.all()

    context = {'stores': queryset}

    return render(request, 'products/stores_list.html', context)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid():
        form.save()
    context = {'form': form}

    return render(request, 'products/create_product.html', context=context)
