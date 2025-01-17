# Core Django imports
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)

# app imports
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

# third-party packages
from taggit.models import Tag


def post_home(request):
    """
    Function view to render the home page
    """
    template_name = "posts/home.html"
    return render(request, template_name)

def post_about(request):
    """
    Function view to render the about page
    """
    template_name = "posts/about.html"
    return render(request, template_name)

def post_list(request, subject=None, tag_slug=None):
    """
    Function view to render posts on the basis of
    subject or tags passed to the url
    """
    posts = Post.published.all()
    if subject:
        if not subject == 'all':
            posts = Post.published.filter(subject=subject)
    elif tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    ## pagination
    paginator = Paginator(posts, 2) # 2 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page
        posts = paginator.page(paginator.num_pages)

    template_name = "posts/list.html"
    context = {
            'object_list': posts,
            'page': page,
            }
    return render(request, template_name, context)

def post_detail(request, year, month, day, post_slug):
    """
    Function view for a single post
    """
    post = get_object_or_404(Post, title_slug=post_slug,
                                   status='published',
                                   created__year=year,
                                   created__month=month,
                                   created__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # a comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Don't save to db yet, only create an object
            new_comment = comment_form.save(commit=False)
            # Assign the curent post to the comment
            new_comment.post = post
            # Finally, save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    ## similar posts based on tags
    # flat means give single values and not tuples
    post_tags_ids = post.tags.values_list('id', flat=True) 
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                         .exclude(id=post.id)
    # use the Count function to generate the same_tags field
    # which contains number of tags shared with all of the tags queried
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags', '-created')[:4]
    # display the latest posts based on no. of shared tags


    return render(request, template_name='posts/detail.html',\
                           context={'post': post,
                                    'comments': comments,
                                    'new_comment': new_comment,
                                    'comment_form': comment_form,
                                    'similar_posts': similar_posts} )

def post_share(request, post_id):
    """
    Function view to handle the email form and send an email
    """
    # retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # if a form was submitted
        form = EmailPostForm(data=request.POST)
        if form.is_valid():
            # get a dict of valid fields and their value
            clean_data = form.cleaned_data
            # use the value inside clean_data to build our email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{clean_data['name']} recommends you check out {post.title}"
            message = f"Check out {post.title} at {post_url}\n\n"\
                      f"{clean_data['name']}\'s comments: {clean_data['comments']}"
            sent = True
            send_mail(subject, message, 'pratikdevkota82@gmail.com', [clean_data['to']])
    else:
        form  = EmailPostForm()
    return render(request, template_name='posts/share.html',\
                 context={ 'post': post, 'form': form, 'sent': sent })
