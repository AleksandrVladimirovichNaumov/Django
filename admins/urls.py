from django.urls import path

from .views import index, UserListView, UserUpdateView, UserCreateView, UserDeleteView, CategoryListView, \
    CategoryCreateView, CategoryUpdateView, CategoryDeleteView, ProductListView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView

app_name = 'admins'
urlpatterns = [

    path('', index, name='index'),

    path('user/', UserListView.as_view(), name='admins_user'),
    path('user-create/', UserCreateView.as_view(), name='admins_user_create'),
    path('user-update/<int:pk>/', UserUpdateView.as_view(), name='admins_user_update'),
    path('user-delete/<int:pk>/', UserDeleteView.as_view(), name='admins_user_delete'),

    path('category/', CategoryListView.as_view(), name='admins_category'),
    path('category-create/', CategoryCreateView.as_view(), name='admins_category_create'),
    path('category-update/<int:pk>/', CategoryUpdateView.as_view(), name='admins_category_update'),
    path('category-delete/<int:pk>/', CategoryDeleteView.as_view(), name='admins_category_delete'),

    path('product/', ProductListView.as_view(), name='admins_product'),
    path('product-create/', ProductCreateView.as_view(), name='admins_product_create'),
    path('product-update/<int:pk>/', ProductUpdateView.as_view(), name='admins_product_update'),
    path('product-delete/<int:pk>/', ProductDeleteView.as_view(), name='admins_product_delete'),
]
