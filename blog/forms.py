from django import forms

from blog.models import BlogPost
from users.forms import StyleFormMixin


class BlogPostForm(StyleFormMixin, forms.ModelForm):

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    class Meta:
        model = BlogPost
        fields = ('title', 'content', 'preview_image', 'is_published')
