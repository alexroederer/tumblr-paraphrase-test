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

    postMarker = 0

    def __init__(self, blogName): 
        self.blogName = blogName
        # When starting, to ensure this is a valid non-empty blog, i
        # attempt to get posts. Return: dict
        post = client.posts(blogName, limit=1)
        # TODO: Make more detailed error handling; meta tag provides error details. 
        if 'meta' in post: 
            # Raise exception
            raise Exception('Blog not found')
        else:
            # Store blog information
            self.blogInfo = post['blog']
            self.totalPosts = post['total_posts']

    def getTitle(self):
        return self.blogInfo['title']

    # Checks if there are more unseen posts
    def isMorePosts(self):
        return postMarker < self.totalPosts

    # Retrieves next posts available; keeps track of what's been seen already
    def getMorePosts(self, numberToRetrieve):
        # No more posts available
        if not self.isMorePosts(): 
            return []
        posts = client.posts(self.blogName, limit=numberToRetrieve, offset=self.postMarker)
        # We will assume at this point the blog exists
        self.postMarker += len(posts['posts'])
        return posts['posts']

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
            return '', ''
        elif post['type'] == 'quote':
            return '', ''
        elif post['type'] == 'link':
            return '', ''
        elif post['type'] == 'answer':
            return '', ''
        elif post['type'] == 'video':
            return '', ''
        elif post['type'] == 'chat':
            return '', ''
        else:
            return '', ''