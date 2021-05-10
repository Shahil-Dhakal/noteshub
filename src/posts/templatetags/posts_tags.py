""" File defining custom template tags for our project """

# Core Django imports
from django import template

# app-imports
from posts.models import Post


register = template.Library()

@register.simple_tag
def total_posts():
    """ 
    A simple template tag that shows the number
    of posts that have been uploaded so far 
    """
    return Post.published.count()

@register.inclusion_tag('posts/latest_uploads.html')
def show_latest_uploads(count=3):
    """
    An inclusion template tag that renders the latest_uploads.html template
    with context variables including the latest uploads.
    The number of latest uploads to display can be passed to the tag
    as the value of the 'count' variable.
    """
    latest_uploads = Post.published.order_by('-created')[:count]
    return { 'latest_uploads': latest_uploads }
