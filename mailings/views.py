from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, \
    UpdateView, DeleteView, TemplateView
from django.core.cache import cache

from blog.models import BlogPost
from mailings.forms import MailingSettingsForm, ClientsForm, MessagesForm
from mailings.models import MailingSettings, Clients, Log, Messages


class MailingSettingsCreateView(LoginRequiredMixin,
                                PermissionRequiredMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm

    permission_required = 'mailings.add_mailingsettings'
    success_url = reverse_lazy('mailings:list')

    def get_form_kwargs(self):
        kwargs = super(MailingSettingsCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingSettingsUpdateView(LoginRequiredMixin,
                                PermissionRequiredMixin, UpdateView):
    model = MailingSettings
    fields = ('start_date', 'end_date', 'periodicity', 'message', 'clients')
    permission_required = 'mailings.change_mailingsettings'
    success_url = reverse_lazy('mailings:list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user \
                and not self.request.user.is_staff:
            raise Http404
        return self.object


class MailingSettingsListView(LoginRequiredMixin, ListView):
    model = MailingSettings
    extra_context = {
        'title': 'Список рассылок'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset


class MailingSettingsDetailView(LoginRequiredMixin, DetailView):
    model = MailingSettings

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mailings_item = MailingSettings.objects.get(pk=self.kwargs.get('pk'))
        context_data['pk'] = mailings_item.pk
        context_data['title'] = 'Рассылка ID ' + str(mailings_item.pk)
        return context_data


class MailingSettingsDeleteView(LoginRequiredMixin,
                                PermissionRequiredMixin, DeleteView):
    model = MailingSettings
    permission_required = 'mailings.delete_mailingsettings'
    success_url = reverse_lazy('mailings:list')


class ClientsCreateView(LoginRequiredMixin,
                        PermissionRequiredMixin, CreateView):
    model = Clients
    form_class = ClientsForm
    # fields = ('email', 'fullname', 'comment')
    permission_required = 'mailings.add_clients'
    success_url = reverse_lazy('mailings:list_client')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientsUpdateView(LoginRequiredMixin,
                        PermissionRequiredMixin, UpdateView):
    model = Clients
    fields = ('email', 'fullname', 'comment')
    permission_required = 'mailings.change_clients'
    success_url = reverse_lazy('mailings:list_client')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user \
                and not self.request.user.is_staff:
            raise Http404
        return self.object


class ClientsListView(LoginRequiredMixin, ListView):
    model = Clients
    extra_context = {
        'title': 'Список клиентов'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = super().get_queryset().filter(owner=self.request.user)

        return queryset


class ClientsDetailView(LoginRequiredMixin, DetailView):
    model = Clients

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        clients_item = Clients.objects.get(pk=self.kwargs.get('pk'))
        context_data['pk'] = clients_item.pk
        context_data['title'] = 'Клиент:  ' + clients_item.fullname
        return context_data


class ClientsDeleteView(LoginRequiredMixin,
                        PermissionRequiredMixin, DeleteView):
    model = Clients
    permission_required = 'mailings.delete_clients'
    success_url = reverse_lazy('mailings:list_client')


class LogListView(LoginRequiredMixin, ListView):
    model = Log
    extra_context = {
        'title': 'Отчет проведенных рассылок'
    }

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if not self.request.user.is_staff:
            mailings = MailingSettings.objects.filter(owner=self.request.user)
            logs_set = set([])
            for mailing in mailings:
                logs = Log.objects.filter(mailing=mailing)
                logs_set = logs_set.union(logs)
        else:
            logs_set = Log.objects.all()

        context_data['object_list'] = logs_set
        return context_data


@login_required
def get_mailing_logs(request, pk):
    mailing_pk = pk

    context = {
        'object_list': Log.objects.filter(mailing_id=mailing_pk),
        'title': 'Логи рассылки'
    }
    return render(request, 'mailings/mailing_logs.html', context)


# @login_required
def disable_mailing(request, pk):
    mailing = MailingSettings.objects.get(pk=pk)
    mailing.is_active = False
    mailing.save()

    context = {
        'object': mailing
    }
    return render(request, 'mailings/disable_mailing.html', context)


def enable_mailing(request, pk):
    mailing = MailingSettings.objects.get(pk=pk)
    mailing.is_active = True
    mailing.save()

    context = {
        'object': mailing
    }
    return render(request, 'mailings/enable_mailing.html', context)


class IndexView(TemplateView):
    template_name = 'mailings/index.html'
    extra_context = {
        'title': 'Главная страница'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['count_mailing'] = MailingSettings.objects.all().count()
        context_data['count_active_mailing'] = \
            MailingSettings.objects.filter(is_active=True).count()
        context_data['count_user'] = Clients.objects.all().count()

        if settings.CACHE_ENABLED:
            key = 'object_list'
            object_list = cache.get(key)
            if object_list is None:
                object_list = BlogPost.objects.all()[:3]
                cache.set(key, object_list)
        else:
            object_list = BlogPost.objects.all()[:3]

        context_data['object_list'] = object_list
        return context_data


class MessagesCreateView(LoginRequiredMixin, CreateView):
    model = Messages
    form_class = MessagesForm
    success_url = reverse_lazy('mailings:list_messages')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessagesListView(LoginRequiredMixin, ListView):
    model = Messages
    extra_context = {
        'title': 'Сообщения'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = super().get_queryset().filter(owner=self.request.user)

        return queryset


class MessagesUpdateView(LoginRequiredMixin, UpdateView):
    model = Messages
    form_class = MessagesForm
    success_url = reverse_lazy('mailings:list_messages')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user \
                and not self.request.user.is_staff:
            raise Http404
        return self.object


class MessagesDeleteView(LoginRequiredMixin, DeleteView):
    model = Messages
    success_url = reverse_lazy('mailings:list_messages')
