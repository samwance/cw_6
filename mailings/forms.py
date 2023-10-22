from django import forms
from mailings.models import MailingSettings, Clients, Messages
from users.forms import StyleFormMixin


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('user', None)
        super(MailingSettingsForm, self).__init__(*args, **kwargs)

        self.fields['clients'].queryset = Clients.objects.filter(owner=owner)
        self.fields['message'].queryset = Messages.objects.filter(owner=owner)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    class Meta:
        model = MailingSettings
        fields = (
            'start_date',
            'end_date',
            'periodicity',
            'message',
            'clients'
        )


class ClientsForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Clients
        fields = ('email', 'fullname', 'comment')


class MessagesForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Messages
        fields = ('subject', 'content')
