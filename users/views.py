import random

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView

from users.forms import UserRegisterForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:expectation')
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save()
        email = user.email
        pk = user.pk
        user.is_active = False
        code = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        user.code = code
        user.save()
        url = f'http://127.0.0.1:8000/users/{pk}/verification/{code}'
        send_mail(
            subject='Подтверждение регистрации',
            message=f'Для подтверждения регистрации перейдите по ссылке {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )
        return super().form_valid(form)


class VerificationView(TemplateView):
    template_name = 'users/verification.html'
    extra_context = {
        'title': 'Поздравляем! Вы успешно зарегистрировались'
    }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs.get('pk'))
        if user:
            user.is_active = True
            user.save()
        return self.render_to_response(context)


def expectation(request):
    context = {
        'title': 'Подтверждения регистрации'
    }
    return render(request, 'users/expectation.html', context)


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    extra_context = {
        'title': 'Пользователи'
    }
    permission_required = 'users.view_user'

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_staff=True)

        return queryset


def block_user(request, pk):
    user = User.objects.get(pk=pk)
    user.is_active = False
    user.save()
    context = {
        'object': user
    }
    return render(request, 'users/block_user.html', context)


def unblock_user(request, pk):
    user = User.objects.get(pk=pk)
    user.is_active = True
    user.save()
    context = {
        'object': user
    }
    return render(request, 'users/unblock_user.html', context)
