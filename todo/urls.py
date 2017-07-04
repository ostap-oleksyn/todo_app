from django.conf.urls import url
from django.contrib.auth.decorators import login_required
import django.contrib.auth.views as auth_view
from django.urls import reverse_lazy

from .views import (Home, TaskEdit, delete, done, Login, login_redirect)

urlpatterns = [
    url(r'^$', login_redirect),
    url(r'^login', Login.as_view(), name='login'),
    url(r'^home/', login_required(Home.as_view()), name='home'),
    url(r'^(?P<pk>[\w-]+)/edit/', login_required(TaskEdit.as_view()), name='edit'),
    url(r'^(?P<pk>[\w-]+)/delete/', login_required(delete), name='delete'),
    url(r'^(?P<pk>[\w-]+)/done/', login_required(done), name='done'),
    url(r'^logout/', auth_view.LogoutView.as_view(next_page=reverse_lazy('todo:login')), name='logout'),
]
