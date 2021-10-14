import django.shortcuts

from products.models import Product, ProductCategory
from geekshop.settings import MEDIA_URL
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def index(request):
    context = {
        'title': 'geekshop'
    }
    return django.shortcuts.render(request, 'products/index.html', context)


def products(request, category_id=None, page_id=1):
    products = Product.objects.filter(category_id=category_id) if category_id != None else Product.objects.all()

    paginator = Paginator(products, per_page=3)
    try:
        products_paginator = paginator.page(page_id)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'img_dir': MEDIA_URL,
        'title': 'каталог',
        'categories': ProductCategory.objects.all(),
        'products': products_paginator

    }

    context.update({'products':products_paginator})
    return django.shortcuts.render(request, 'products/products.html', context)
