from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView


class OrderList(ListView):
    pass


class OrderItemsCreate(CreateView):
    pass


class OrderItemsUpdate(UpdateView):
    pass


class OrderItemsDelete(DeleteView):
    pass


class OrderDetail(DetailView):
    pass


def order_forming_complete(request, pk):
    pass