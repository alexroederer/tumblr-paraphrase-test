from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /archivefind/proprietous/, used to access a particular blog
    url(r'^(?P<blog_name>[A-Za-z0-9\-]+)/$', views.blog, name='blog'),
    # /archivefind/
    url(r'^$', views.index, name='index'),
]
