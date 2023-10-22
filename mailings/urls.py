from django.urls import path
from django.views.decorators.cache import cache_page

from mailings.apps import MailingsConfig
from mailings.views import MailingSettingsListView, \
    MailingSettingsCreateView, MailingSettingsUpdateView, \
    MailingSettingsDetailView, MailingSettingsDeleteView, \
    ClientsDeleteView, ClientsDetailView, ClientsUpdateView, \
    ClientsCreateView, ClientsListView, LogListView, get_mailing_logs, \
    IndexView, disable_mailing, enable_mailing, \
    MessagesCreateView, MessagesListView, MessagesUpdateView, \
    MessagesDeleteView

app_name = MailingsConfig.name


urlpatterns = [
    path('list/', MailingSettingsListView.as_view(), name='list'),
    path('list_messages/', MessagesListView.as_view(), name='list_messages'),
    path('create/', MailingSettingsCreateView.as_view(), name='create'),
    path('create_message/', MessagesCreateView.as_view(),
         name='create_message'),
    path('edit/<int:pk>', MailingSettingsUpdateView.as_view(), name='edit'),
    path('edit_message/<int:pk>', MessagesUpdateView.as_view(),
         name='edit_message'),
    path('view/<int:pk>', MailingSettingsDetailView.as_view(), name='view'),
    path('delete/<int:pk>', MailingSettingsDeleteView.as_view(),
         name='delete'),
    path('list_client/', ClientsListView.as_view(), name='list_client'),
    path('create_client/', ClientsCreateView.as_view(), name='create_client'),
    path('edit_client/<int:pk>', ClientsUpdateView.as_view(),
         name='edit_client'),
    path('view_client/<int:pk>', ClientsDetailView.as_view(),
         name='view_client'),
    path('delete_client/<int:pk>', ClientsDeleteView.as_view(),
         name='delete_client'),
    path('delete_message/<int:pk>', MessagesDeleteView.as_view(),
         name='delete_message'),
    path('log', LogListView.as_view(), name='log'),
    path('view/<int:pk>/logs', get_mailing_logs, name='mailing_logs'),
    path('<int:pk>/disable_mailing', disable_mailing, name='disable_mailing'),
    path('<int:pk>/enable_mailing', enable_mailing, name='enable_mailing'),
    path('', cache_page(60)(IndexView.as_view()), name='index'),
]
