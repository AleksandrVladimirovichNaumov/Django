from django.urls import path

from .views import index, UserListView, UserUpdateView, UserCreateView, UserDeleteView

app_name = 'admins'
urlpatterns = [

    path('', index, name='index'),
    path('user/', UserListView.as_view(), name='admins_user'),
    path('user-create/', UserCreateView.as_view(), name='admins_user_create'),
    path('user-update/<int:pk>/', UserUpdateView.as_view(), name='admins_user_update'),
    path('user-delete/<int:pk>/', UserDeleteView.as_view(), name='admins_user_delete'),

]
