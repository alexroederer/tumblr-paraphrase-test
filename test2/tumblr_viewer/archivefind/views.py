from django.shortcuts import render, render_to_response
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
    print "BLOG VIEW"
    try:
        manager = TumblrBlogManager(blog_name)
        posts = manager.getMorePosts(16)
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
        #Record object in session: this may be dangerous, 
        #because if the session in the object contains any information 
        #about the secret keys, that could lead to attacks

    except Exception as e:
        print "EXCEPTION:" 
        print e
        blog_name = None 
        context = {}
    return render(request, 'archivefind/blog.html', context)

def blog_content(request, blog_name): 
    try:
        manager = TumblrBlogManager(blog_name)
        posts = manager.getMorePosts(16)
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
    except Exception as e:
        print "EXCEPTION:" 
        print e
        blog_name = None 
        context = {}
    return render_to_response('archivefind/blog-content.html', context)
