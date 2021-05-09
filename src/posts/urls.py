# core django imports
from django.urls import path

# app imports
from .views import post_home, post_list, post_detail, post_share, post_about


app_name = 'posts'
urlpatterns = [
        path(
            route = '',
            view  = post_home,
            name  = 'posts_home'),

        path(
            route = 'subjects/<str:subject>/',
            view  = post_list,
            name  = 'posts_list_subject'),

        path(
            route = 'tags/<slug:tag_slug>/',
            view  = post_list,
            name  = 'posts_list_tags'),

        path(
            route = 'post/<int:year>/<int:month>/<int:day>/<slug:post_slug>/',
            view  = post_detail,
            name  = 'posts_detail'),

        path(
            route = '<int:post_id>/share/',
            view  = post_share,
            name  = 'posts_share'),
        
        path(
            route = 'about/',
            view  = post_about,
            name  = 'posts_about'),
]
