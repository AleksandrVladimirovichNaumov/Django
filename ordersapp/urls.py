from django.urls import path

from .views import OrderItemsCreate, OrderList, OrderDetail, OrderItemsDelete, OrderItemsUpdate, order_forming_complete

app_name = 'ordersapp'
urlpatterns = [

    path('', OrderList.as_view(), name='list'),
    path('create/', OrderItemsCreate.as_view(), name='create'),
    path('update/<int:pk>/', OrderItemsUpdate.as_view(), name='update'),
    path('read/<int:pk>/', OrderDetail.as_view(), name='read'),
    path('delete/<int:pk>/', OrderItemsDelete.as_view(), name='delete'),
    path('delete/<int:pk>/', order_forming_complete, name='forming_complete'),

]
