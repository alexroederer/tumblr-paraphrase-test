#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#test_1.py
#@author Alexander Roederer
#
#A test of the Tumblr API. 
#
#Test 1: Retrieve the last 16 posts from a blog. 
#Create a little webpage that displays them, a la the 
#native tumblr archive, but in a 4x4 square. 

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
numPostsFetched = 16
allPosts = client.posts('proprietous', limit=numPostsFetched)

#allPosts['blog']           #Gives blog info
#allPosts['total_posts']    #Gives count of all posts made by blog
postList = allPosts['posts']#Gives list of posts

#Iterate throught the posts, collecting all thumbnails
thumbnailURLs = []
postURLs = []
for post in postList:
    #Get photo posts only
    if post['type'] == 'photo':
        #print post['photos'][0] #Prints photo info dict for first photo
        #print post['photos'][0]['alt_sizes'][5] #Square photo thumbnail
        for thumb in post['photos'][0]['alt_sizes']:
            if thumb['width'] == 75:
                thumbnailURLs.append(thumb['url'].encode('utf-8'))
                postURLs.append(post['post_url'].encode('utf-8'))
    elif post['type'] == 'audio':
        thumbnailURLs.append(post['album_art'].encode('utf-8'))
        postURLs.append(post['post_url'].encode('utf-8'))
    else:
        print "NON PHOTO POST ENCOUNTERED"

#Insert thumbnails into html template
htmlTemplate = './test_1.template'
htmlPage = './test_1.html'
numCols = 4
with open(htmlTemplate, 'r') as templateHandle, open(htmlPage, 'w') as outHandle:
    for line in templateHandle:
        line = line.strip()
        print line
        if line == '%ICONS':
            for i, (thumb,link) in enumerate(zip(thumbnailURLs, postURLs)):
                if i % numCols == 0:
                    outHandle.write('      <div class=colBlock>\n')
                outHandle.write('        <a href="'+link+'"><img class=thumbBlock src="'+thumb+'"/></a>\n')
                if i % numCols == (numCols - 1):
                    outHandle.write('      </div>\n')
                outHandle.write('')
        else:
            outHandle.write(line)



