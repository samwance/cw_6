from django.contrib import admin

from mailings.models import MailingSettings, Clients, Messages, Log


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'start_date', 'end_date', 'status', )
    list_filter = ('status',)


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'fullname', 'email', )


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject',)
    search_fields = ('subject', 'content',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'mailing', 'timestamp', 'status', 'response')
    list_filter = ('status',)
