from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, \
    VerificationView, expectation, UserListView, block_user, \
    unblock_user

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    path(
        '<int:pk>/verification/<code>',
        VerificationView.as_view(),
        name='verification'
    ),
    path('expectation', expectation, name='expectation'),
    path('list_users', UserListView.as_view(), name='list_users'),
    path('<int:pk>/block_user', block_user, name='block_user'),
    path('<int:pk>/unblock_user', unblock_user, name='unblock_user'),
]
