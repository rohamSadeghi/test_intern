from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from products.forms import ProductForm, RateForm, BookmarkForm
from products.models import Product, Store, ProductRating, Category, ProductBookmark


def home(request):
    """
    home template view
    :param request: request
    :return: render
    """
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
        context['authenticated'] = self.request.user and self.request.user.is_authenticated
        return context

class ProductDetailView(DetailView):
    template_name = "products/product_detail.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        if user and user.is_authenticated:
            product = self.get_object()
            context['bookmark'] = False
            try:
                context['bookmark'] = ProductBookmark.objects.get(user=user, product=product).like_status
            except ProductBookmark.DoesNotExist:
                pass
            return context


class ProductCreateView(CreateView):
    template_name = "products/create_product.html"
    form_class = ProductForm
    model = Product


class ProductUpdateView(UpdateView):
    template_name = "products/create_product.html"
    form_class = ProductForm
    model = Product

class RateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = ProductRating
    form_class = RateForm
    template_name = "products/product_rate_create.html"

    def get_success_url(self):
        return reverse('products-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = get_object_or_404(Product, id=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        user = self.request.user
        product = self.get_context_data()['product']
        ProductRating.objects.update_or_create(
            user=user,
            product=product,
            defaults={
                'rate':
                    form.cleaned_data['rate']
            }
        )
        return HttpResponseRedirect(self.get_success_url())


class RateDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductRating
    login_url = reverse_lazy('login')
    template_name = 'products/rate_delete.html'


    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(ProductRating, **{'user': self.request.user, 'id': self.kwargs.get('pk')})
        obj.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('products-list')


class CategoryListView(ListView):
    model = Category
    template_name = 'products/category_list.html'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'products/category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        products_properties = {}
        category = self.get_object()

        for p in category.properties:
            products_properties[p] = category.products.values_list(f'properties__{p}', flat=True)
        context['properties'] = products_properties
        return context


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class BookmarkCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    form_class = BookmarkForm
    model = ProductBookmark
    template_name = 'products/create_bookmark.html'

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        user = self.request.user
        ProductBookmark.objects.update_or_create(
            user=user,
            product=product,
            defaults={"like_status": form.cleaned_data.get('like_status', False)}
        )
        return HttpResponseRedirect(self.get_success_url())
