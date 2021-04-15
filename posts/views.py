# Core Django imports
from django.shortcuts import render
from django.views.generic import ListView

# app imports
from .models import Post



class HomeView(ListView):
    """
    Class view for our home page
    """
    model = Post
    template_name = "posts/post_home.html" # <app>/<model>_<viewtype>.html

    def get_context_data(self, **kwargs):
        """
        Returns the context to which we're displaying the posts
        """
        context = super(HomeView, self).get_context_data(**kwargs)
        context['all_posts'] = Post.objects.all()
        return context
