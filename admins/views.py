from django.contrib.auth.decorators import user_passes_test
from django.db import connection
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, CategoryAdminCreateForm, CategoryAdminUpdateForm, \
    CreateAdminProductForm, ProductAdminUpdateForm
from geekshop.mixin import CustomDispatchMixin
from products.models import ProductCategory, Product
from users.models import User


def index(request):
    return render(request, 'admins/admin.html')


class UserListView(ListView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-read.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'Панель Администратора | Пользователи'
        return context


class UserCreateView(CreateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Панель Администратора | Регистрация'
        return context


class UserUpdateView(UpdateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Панель Администратора | Обновление пользователя'
        return context


class UserDeleteView(DeleteView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-read.html'
    success_url = reverse_lazy('admins:admins_user')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = not self.object.is_active
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CategoryListView(ListView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-categories-read.html'
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Панель Администратора | Категории'
        return context


class CategoryCreateView(CreateView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-categories-create.html'
    form_class = CategoryAdminCreateForm
    success_url = reverse_lazy('admins:admins_category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Панель Администратора | Добавление категории'
        return context


class CategoryUpdateView(UpdateView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-categories-update-delete.html'
    # from_class = CategoryAdminUpdateForm
    # context_object_name = 'category'
    # fields = '__all__'
    success_url = reverse_lazy('admins:admins_category')

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Панель Админимтратора | Обновление категории'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price')*(1-discount/100))
                # db_profile_by_type(self.__class__, 'update', connection.queries)
        return HttpResponseRedirect(self.get_success_url())



class CategoryDeleteView(DeleteView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-categories-read.html'
    context_object_name = 'category'

    fields = '__all__'
    success_url = reverse_lazy('admins:admins_category')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = not self.object.is_active
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductListView(ListView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-products-read.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Панель Администратора | Продукты'
        return context


class ProductCreateView(CreateView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-products-create.html'
    form_class = CreateAdminProductForm
    success_url = reverse_lazy('admins:admins_product')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Панель Администратора | Добавление продукта'
        return context

class ProductUpdateView(UpdateView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-update-delete.html'
    from_class = ProductAdminUpdateForm
    context_object_name = 'product'
    fields = ('name', 'description', 'quantity', 'price', 'category', 'image')
    success_url = reverse_lazy('admins:admins_product')

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Панель Админимтратора | Обновление продукта'
        return context


class ProductDeleteView(DeleteView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-products-read.html'
    context_object_name = 'product'

    fields = '__all__'
    success_url = reverse_lazy('admins:admins_product')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = not self.object.is_active
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())