import pytumblr
from tumblr_keys import *

# Authenticate
client = pytumblr.TumblrRestClient(
    consumer_key,
    consumer_secret,
    token_key, 
    token_secret
    )

class TumblrBlogManager:

    MAX_LIMIT_RETRIEVE = 16

    def __init__(self, blogName, postMarker=0): 
        self.blogName = blogName
        self.postMarker = postMarker
        self.tagsList = []
        # When starting, to ensure this is a valid non-empty blog, i
        # attempt to get posts. Return: dict
        post = client.posts(blogName, limit=1)
        # TODO: Make more detailed error handling; meta tag provides error details. 
        if 'meta' in post and post['meta']['status'] == 404: 
            # Raise exception
            raise Exception('Blog not found')
        else:
            # Store blog information
            self.blogInfo = post['blog']
            self.totalPosts = post['total_posts']

    def getTitle(self):
        return self.blogInfo['title']

    # Sets a filter for posts; only posts with these tags will be returned
    def setTagFilter(self, tagsList):
        self.tagsList = tagsList

    def clearTagFilter(self):
        self.tagsList = []

    # Checks if there are more unseen posts
    def isMorePosts(self):
        return self.postMarker < self.totalPosts

    # Retrieves next posts available; keeps track of what's been seen already
    # Only returns posts that conform to current filters
    def getMorePosts(self, numberToRetrieve):
        postsToReturn = []
        numberRetrieved = 0

        #howFarBack = 

        while self.isMorePosts() and numberRetrieved < numberToRetrieve: 
            # Attempt to get more posts
            # API retrieval is limited to a number of posts at a time
            # If we request fewer, though, we only want to return that many
            retrieveLimit = min(self.MAX_LIMIT_RETRIEVE, numberToRetrieve-numberRetrieved)
            posts = client.posts(self.blogName, limit=retrieveLimit, offset=self.postMarker)
            # Keep track of the global post marker
            self.postMarker += len(posts['posts'])
            # Keep track of how many posts that conform to filter limits we've 
            # successfully found
            goodPosts = []
            for post in posts['posts']: 
                if len(self.tagsList) != 0: 
                    # Check to see if this post has all the tags we want
                    if len(set(self.tagsList) & set(post['tags'])) == len(self.tagsList): 
                        goodPosts.append(post)
                else:
                    goodPosts.append(post)

            print len(goodPosts)
            numberRetrieved += len(goodPosts)
            postsToReturn.extend(goodPosts)

        return postsToReturn

    def getRecentPosts(self, numberToRetrieve): 
        posts = client.posts(self.blogName, limit=numberToRetrieve, offset=self.postMarker)
        return posts['posts']

    def resetPostPosition(self):
        self.postMarker = 0

    # Returns a thumbnail and a post URL
    def processPost(self, post):
        enc = 'utf-8'
        if post['type'] == 'photo':
            for thumb in post['photos'][0]['alt_sizes']:
                if thumb['width'] == 75:
                    return thumb['url'].encode(enc), post['post_url'].encode(enc)
        elif post['type'] == 'audio':
            return post['album_art'].encode(enc), post['post_url'].encode(enc)
        elif post['type'] == 'text':
            return '', post['post_url'].encode(enc) 
        elif post['type'] == 'quote':
            return '', post['post_url'].encode(enc)
        elif post['type'] == 'link':
            if 'photos' in post:
                for thumb in post['photos'][0]['alt_sizes']:
                    if thumb['width'] == 75:
                        return thumb['url'].encode(enc), post['post_url'].encode(enc)
            return '', post['post_url'].encode(enc) 
        elif post['type'] == 'answer':
            return '', post['post_url'].encode(enc)
        elif post['type'] == 'video':
            if 'photos' in post:
                for thumb in post['photos'][0]['alt_sizes']:
                    if thumb['width'] == 75:
                        return thumb['url'].encode(enc), post['post_url'].encode(enc)
            return '', post['post_url'].encode(enc) 
        elif post['type'] == 'chat':
            return '', post['post_url'].encode(enc) 
        else:
            return '', ''
