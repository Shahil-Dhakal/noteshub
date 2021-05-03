# core django imports
from django.urls import path

# app imports
from .views import post_home, post_subject, post_detail, post_share, post_about


app_name = 'posts'
urlpatterns = [
        path(
            route = '',
            view  = post_home,
            name  = 'posts_home'),

        path(
            route = 'subjects/<str:subject>/',
            view  = post_subject,
            name  = 'posts_subject'),

        path(
            route = '<int:year>/<int:month>/<int:day>/<slug:post_slug>/',
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
