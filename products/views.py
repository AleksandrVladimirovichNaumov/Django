import django.shortcuts
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from products.models import Product, ProductCategory
from geekshop.settings import MEDIA_URL
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

class ProductsListView(ListView):
    model = Product
    title = 'Каталог'
    template_name = 'products/products.html'
    # Выводим по три объекта на страницу
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        context['page_quantity'] = range(1, len(self.object_list)//self.paginate_by+2)
        context['page_max'] = len(self.object_list)//self.paginate_by+1
        # флаг для првоерки отфильтрованы ли продукты по категории
        context['is_categorised'] = True if self.kwargs.get('category_id') else False
        if self.kwargs.get('page_id'):
            context['page_obj'].number = self.kwargs.get('page_id')
            context['page_obj'].object_list = self.object_list[context['page_obj'].number * self.paginate_by - self.paginate_by:self.paginate_by * context['page_obj'].number]
        # как оказалось нельзя фильтровать срезы после пагинации.
        # поэтому сначала фильтруем все объекты а потом делаем срез в зависимости от текущей страницы и шага пагинатора
        if self.kwargs.get('category_id'):
            context['current_category'] = self.kwargs.get('category_id')
            if self.kwargs.get('page_id'):
                context['page_obj'].number = self.kwargs.get('page_id')
            filtered_page_obj = self.object_list.filter(category_id=self.kwargs['category_id'])
            context['page_quantity'] = range(1, len(filtered_page_obj) // self.paginate_by + 2)
            context['page_max'] = len(filtered_page_obj) // self.paginate_by + 1
            # делаем срез в зависимости от текущей страницы и шага пагинатора
            context['page_obj'].object_list = filtered_page_obj[context['page_obj'].number*self.paginate_by - self.paginate_by:self.paginate_by*context['page_obj'].number]
        return context

    def get_price(self, pk):
        return JsonResponse({'price': Product.objects.get(pk=pk).get_product_price()})


class ProductsIndex(ListView):
    model = Product
    title = 'Каталог'
    template_name = 'products/index.html'
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
