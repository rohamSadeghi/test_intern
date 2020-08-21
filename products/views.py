from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from products.forms import ProductForm, RateForm
from products.models import Product, Store, ProductRating


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


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/products_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['numbers'] = ['a', 'b']
        return context

class ProductDetailView(DetailView):
    template_name = "products/product_detail.html"
    model = Product


class ProductCreateView(CreateView):
    template_name = "products/create_product.html"
    form_class = ProductForm
    model = Product


class ProductUpdateView(UpdateView):
    template_name = "products/create_product.html"
    form_class = ProductForm
    model = Product

class RateView(CreateView):
    model = ProductRating
    form_class = RateForm
    template_name = "products/product_rate_create.html"

    # def form_valid(self, form):
    #     super().form_valid(form=form)
    #     user = self.request.user
    #     product = get_object_or_404(Product, id=self.kwargs.get('pk'))
    #     form.cleaned_data['user'] = user
    #     form.cleaned_data['product'] = product
    #     return form
