from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /archivefind/proprietous/, used to access a particular blog
    url(r'^(?P<blog_name>[A-Za-z0-9\-]+)/$', views.blog, name='blog'),
    # /archivefind/
    url(r'^$', views.index, name='index'),
    url(r'^(?P<blog_name>[A-Za-z0-9\-]+)/blog_content/$', views.blog_content, name='blog_content'),
    url(r'^(?P<blog_name>[A-Za-z0-9\-]+)/search_posts/$', views.search_posts, name='search'),
]
