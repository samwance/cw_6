from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogPostListView, BlogPostDetailView, \
    BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView


app_name = BlogConfig.name

urlpatterns = [
    path('', BlogPostListView.as_view(), name='list'),
    path('create/', BlogPostCreateView.as_view(), name='create'),
    path('edit/<int:pk>', BlogPostUpdateView.as_view(), name='edit'),
    path('view/<int:pk>', cache_page(60)(BlogPostDetailView.as_view()),
         name='view'),
    path('delete/<int:pk>', BlogPostDeleteView.as_view(), name='delete'),
]
