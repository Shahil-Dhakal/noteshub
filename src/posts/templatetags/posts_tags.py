""" File defining custom template tags for our project """

# Core Django imports
from django import template

# app-imports
from posts.models import Post


register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()
