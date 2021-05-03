# Core Django imports
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail

# app imports
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm


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

def post_subject(request, subject):
    """
    Function view to render posts on the basis of
    subject passed to the url
    """
    if subject == 'all':
        posts = Post.published.all()
    else:
        posts = Post.published.filter(subject=subject)
    template_name = "posts/list.html"
    context = {
            'subject_posts': posts,
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

    return render(request, template_name='posts/detail.html',\
                           context={'post': post,
                                    'comments': comments,
                                    'new_comment': new_comment,
                                    'comment_form': comment_form} )

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
            subject = f"{clean_data['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n"\
                      f"{clean_data['name']}\'s comments: {clean_data['comments']}"
            send_mail(subject, message, 'pratikdevkota82@gmail.com', [clean_data['to']])
            sent = True
    else:
        form  = EmailPostForm()
    return render(request, template_name='posts/share.html',\
                 context={ 'post': post, 'form': form, 'sent': sent })
