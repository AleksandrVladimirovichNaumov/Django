
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from users.models import User


def index(request):
    return render(request, 'admins/admin.html')


class UserListView(ListView):
    model=User
    template_name = 'admins/admin-users-read.html'
    context_object_name = 'users'

    def get_context_data(self,  *, object_list = None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title']= 'Панель Админимтратора | Пользователи'
        return context

class UserCreateView(CreateView):
    pass

class UserUpdateView(UpdateView):
    pass

class UserDeleteView(DeleteView):
    pass