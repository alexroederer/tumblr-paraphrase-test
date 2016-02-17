from django.shortcuts import render, render_to_response
from django.http import HttpResponse

import pytumblr
from tumblr_keys import *
from TumblrBlogManager import TumblrBlogManager

NUM_POSTS_LOAD = 16 

# Create your views here.
def createPostsList(manager, posts):
    parsed_posts = []
    for post in posts:
        thumb, url = manager.processPost(post)
        parsed_posts.append({
            'thumb': thumb, 
            'url': url, 
            })
    return parsed_posts

def index(request):
    #Renders the index page
    context = {}
    return render(request, 'archivefind/index.html', context)

def blog(request, blog_name):
    #Renders a preliminary view for a blog of interest. 
    print "BLOG VIEW"
    try:
        manager = TumblrBlogManager(blog_name)
        posts = manager.getMorePosts(NUM_POSTS_LOAD)

        parsed_posts = createPostsList(manager, posts)
        #Prepare context
        context = {
            'blog_name': blog_name, 
            'posts_list': parsed_posts,
        }

        #Manager object cannot be turned into JSON, so 
        #we have to save manager info to reconstruct it 
        #after each transaction
        request.session['blog_name'] = manager.blogName
        request.session['post_marker'] = manager.postMarker 

    except Exception as e:
        print "Exception", e
        blog_name = None 
        context = {}
    return render(request, 'archivefind/blog.html', context)

def blog_content(request, blog_name): 
    #Attempts to pull more of a blog's content. 
    try:
        manager = TumblrBlogManager(request.session['blog_name'], 
            request.session['post_marker'])
        posts = manager.getMorePosts(NUM_POSTS_LOAD)

        parsed_posts = createPostsList(manager, posts)
        context = {
            'blog_name': blog_name, 
            'posts_list': parsed_posts,
        }
        request.session['blog_name'] = manager.blogName
        request.session['post_marker'] = manager.postMarker 

    except Exception as e:
        print "EXCEPTION:", e
        blog_name = None 
        context = {}
    return render_to_response('archivefind/blog-content.html', context)

def search_posts(request, blog_name): 
    print request.POST['tags']
    try: 
        #Note that a new search resets the post marker
        manager = TumblrBlogManager(request.session['blog_name'])
        #Parse tags received (eventually expand to parse all options 
        # available as part of the form
        tagsString = request.POST['tags']
        tagsList = tagsString.split(',')
        tagsList = [tag.strip().strip('#') for tag in tagsList]

        #Set filter on manager
        manager.setTagFilter(tagsList)

        #Now get posts
        posts = manager.getMorePosts(NUM_POSTS_LOAD)
        parsed_posts = createPostsList(manager, posts)
        context = {
            'blog_name': blog_name, 
            'posts_list': parsed_posts,
        }

        request.session['blog_name'] = manager.blogName
        request.session['post_marker'] = manager.postMarker 
    except Exception as e:
        print "EXCEPTION:", e
        blog_name = None
        context = {}

    return render_to_response('archivefind/blog-content.html', context)
