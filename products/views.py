import django.shortcuts
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from feedbacks.models import Feedback
from products.models import Product, ProductCategory
from geekshop.settings import MEDIA_URL
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404


# Create your views here.

class ProductsListView(ListView):
    model = Product
    title = 'Каталог'
    template_name = 'products/products.html'
    # Выводим по три объекта на страницу
    paginate_by = 3

    @staticmethod
    def get_product(pk):
        if settings.LOW_CACHE:
            key = f'product{pk}'
            product = cache.get(key)
            if product is None:
                product = Product.objects.get(pk=pk)
                cache.set(key, product)
            return product
        else:
            return Product.objects.get(pk=pk)

    @staticmethod
    def get_links_category():
        if settings.LOW_CACHE:
            key = 'links_category'
            links_category = cache.get(key)
            if links_category is None:
                links_category = ProductCategory.objects.all()
                cache.set(key, links_category)
            return links_category
        else:
            return ProductCategory.objects.all()

    @staticmethod
    def get_links_product():
        if settings.LOW_CACHE:
            key = 'links_product'
            links_product = cache.get(key)
            if links_product is None:
                links_product = Product.objects.all()
                cache.set(key, links_product)
            return links_product
        else:
            return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['products'] = self.get_links_product()
        context['categories'] = self.get_links_category()
        context['page_quantity'] = range(1, len(self.object_list) // self.paginate_by + 2)
        context['page_max'] = len(self.object_list) // self.paginate_by + 1
        # флаг для првоерки отфильтрованы ли продукты по категории
        context['is_categorised'] = True if self.kwargs.get('category_id') else False
        if self.kwargs.get('page_id'):
            context['page_obj'].number = self.kwargs.get('page_id')
            context['page_obj'].object_list = self.object_list[context[
                                                                   'page_obj'].number * self.paginate_by - self.paginate_by:self.paginate_by *
                                                                                                                            context[
                                                                                                                                'page_obj'].number]
        # как оказалось нельзя фильтровать срезы после пагинации.
        # поэтому сначала фильтруем все объекты а потом делаем срез в зависимости от текущей страницы и шага пагинатора
        if self.kwargs.get('category_id'):
            context['current_category'] = self.kwargs.get('category_id')
            if self.kwargs.get('page_id'):
                context['page_obj'].number = self.kwargs.get('page_id')
            filtered_page_obj = self.object_list.filter(category_id=self.kwargs['category_id']).select_related(
                'category')
            context['page_quantity'] = range(1, len(filtered_page_obj) // self.paginate_by + 2)
            context['page_max'] = len(filtered_page_obj) // self.paginate_by + 1
            # делаем срез в зависимости от текущей страницы и шага пагинатора
            context['page_obj'].object_list = filtered_page_obj[context[
                                                                    'page_obj'].number * self.paginate_by - self.paginate_by:self.paginate_by *
                                                                                                                             context[
                                                                                                                                 'page_obj'].number]
        return context

    def get_price(self, pk):
        return JsonResponse({'price': Product.objects.get(pk=pk).get_product_price()})


class ProductsIndex(ListView):
    model = Product
    title = 'Каталог'
    template_name = 'products/index.html'

class ProductDetailView(ListView):
    model=Product
    title = 'Информация о товаре'
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        context['product'] = ProductsListView.get_product(self.kwargs.get('pk'))
        context['categories'] = ProductCategory.objects.all()
        return context



#
#
#
# def index(request):
#     context = {
#         'title': 'geekshop'
#     }
#     return django.shortcuts.render(request, 'products/index.html', context)


# def products(request, category_id=None, page_id=1):
#     products = Product.objects.filter(category_id=category_id) if category_id != None else Product.objects.all()
#
#     paginator = Paginator(products, per_page=3)
#     try:
#         products_paginator = paginator.page(page_id)
#     except PageNotAnInteger:
#         products_paginator = paginator.page(1)
#     except EmptyPage:
#         products_paginator = paginator.page(paginator.num_pages)
#
#     context = {
#         'img_dir': MEDIA_URL,
#         'title': 'каталог',
#         'categories': ProductCategory.objects.all(),
#         'products': products_paginator
#
#     }
#
#     context.update({'products':products_paginator})
#     return django.shortcuts.render(request, 'products/products.html', context)
