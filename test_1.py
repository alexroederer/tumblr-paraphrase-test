'''
test_1.py
@author Alexander Roederer

A test of the Tumblr API. 

Test 1: Retrieve the last 16 posts from a blog. 
Create a little webpage that displays them, a la the 
native tumblr archive, but in a 4x4 square. 
'''

import pytumblr
from tumblr_keys import *

#Authenticate
client = pytumblr.TumblrRestClient(
    consumer_key, 
    consumer_secret,
    token_key,
    token_secret
)

#Request posts; return type is a dict
allPosts = client.posts('proprietous', limit=16)

#allPosts['blog']           #Gives blog info
#allPosts['total_posts']    #Gives count of all posts made by blog
postList = allPosts['posts']#Gives list of posts

#Iterate throught the posts
for post in postList:
    print post

