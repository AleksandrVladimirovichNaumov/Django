from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites import requests
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy

# Create your views here.
from django.views.generic import FormView, UpdateView

from baskets.models import Basket
from geekshop.mixin import BaseClassContextMixin, CustomDispatchMixin
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
from django.contrib.auth.decorators import login_required

from users.models import User


class LoginLoginView(LoginView, BaseClassContextMixin):
    template_name = 'users/login.html'
    from_class = UserLoginForm
    title = 'Geekshop - Авторизация'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(LoginLoginView, self).get_context_data()
        context['title'] = "Авторизация"
        return context


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#
#     else:
#         form = UserLoginForm()
#
#     context = {
#         'title': 'Geekshop - Авторизация',
#         'form': form
#     }
#     return render(request, 'users/login.html', context)

class RegisterListView(FormView, BaseClassContextMixin):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    title = 'Geekshop - Регистрация'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_verify_link(user):
                messages.success(request, 'Вы успешно зарегистрированы')

            return redirect(self.success_url)
        return redirect(self.success_url)

    def send_verify_link(self, user):
        verify_link = reverse('users:verify', args=[user.email, user.activation_key])
        subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
        message = f'Для подтверждения учетной записи {user.username} на портале \n {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, email, activation_key):
        # try:
            user = User.objects.get(email=email)
            if user and user.activation_key == activation_key and not user.is_activation_key_expired():
                user.activation_key = ''
                user.activation_key_created = None
                user.is_active = True
                user.save()


            auth.login(self, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(self, 'users/verification.html')
        # except Exception as e:
        #     return HttpResponseRedirect(reverse('index'))


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегистрированы')
#             return HttpResponseRedirect(reverse('users:login'))
#
#     else:
#         form = UserRegisterForm()
#
#     context = {
#         'title': 'Geekshop - Регистрация',
#         'form': form
#     }
#     return render(request, 'users/register.html', context)

class Logout(LogoutView, BaseClassContextMixin):
    template_name = 'products/index.html'


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))

class ProfileFormView(UpdateView, BaseClassContextMixin, LoginRequiredMixin):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    title = 'Geekshop - Профиль'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)


    def get_context_data(self, **kwargs):
        context = super(ProfileFormView, self).get_context_data(**kwargs)
        context['profile'] = UserProfileEditForm(instance=self.request.user.userprofile)

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES, instance=request.user)
        userprofile = UserProfileEditForm(data=request.POST, instance=request.user.userprofile)
        if form.is_valid() and userprofile.is_valid():
            form.save()
            return redirect(self.success_url)
        return redirect(self.success_url)


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'профиль сохранен')
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             messages.error(request, 'профиль не сохранен')
#
#     context = {
#         'title': 'Профиль',
#         'form': UserProfileForm(instance=request.user),
#         'baskets': Basket.objects.filter(user=request.user)
#     }
#     return render(request, 'users/profile.html', context)


# def send_verify_link(user):
#     verify_link = reverse('users:verify', args=[user.email, user.activation_key])
#     subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
#     message = f'Для подтверждения учетной записи {user.username} на портале \n {settings.DOMAIN_NAME}{verify_link}'
#     return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)



# def verify(request, email, activation_key):
#     try:
#         user = User.objects.get(email=email)
#         if user and user.activation_key == activation_key and not user.is_activation_key_expired():
#             user.activation_key = ''
#             user.activation_key_created = None
#             user.is_active = True
#             user.save()
#             auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#             # auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#         return render(request, 'users/verification.html')
#     except Exception as e:
#         return HttpResponseRedirect(reverse('index'))
