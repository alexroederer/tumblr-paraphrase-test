from django.shortcuts import render
from django.http import HttpResponse

import pytumblr
from tumblr_keys import *
from TumblrBlogManager import TumblrBlogManager

# Create your views here.

def index(request):
    #Renders the index page
    context = {}
    return render(request, 'archivefind/index.html', context)

def blog(request, blog_name):
    #Renders a preliminary view for a blog of interest. 
    try:
        manager = TumblrBlogManager(blog_name)
        posts = manager.getRecentPosts(16)
        parsed_posts = []
        for post in posts:
            thumb, url = manager.processPost(post)
            parsed_posts.append({
                'thumb': thumb, 
                'url': url, 
                })
        context = {
            'blog_name': blog_name, 
            'posts_list': parsed_posts,
        }
    except Exception:
        blog_name = None 
        context = {}
    return render(request, 'archivefind/blog.html', context)
