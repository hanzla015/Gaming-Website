from django.contrib import messages 
from django.shortcuts import redirect, render
from blog.models import *
from blog.templatetags import extras
import datetime 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def blog(request):

    # week_ago = datetime.date.today()-datetime.timedelta(days=7)
    # trends = Post.objects.filter(time_stamp=week_ago).order_by('read')
    blogs = Post.objects.filter(publish=True).order_by('-time_stamp')
    all_posts = Paginator(object_list = blogs, per_page=12)
    page = request.GET.get('page')
    try:
        posts = all_posts.page(page)
    except PageNotAnInteger:
        posts = all_posts.page(1)
    except EmptyPage:
        posts = all_posts.page(all_posts.num_pages)
    last = all_posts.num_pages    
    context = {'posts': posts,
                'last':last,
    }
    return render(request, 'blog/home.html', context)

def blogPost(request, slug):
    recent_post = Post.objects.all().order_by("-time_stamp")
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    tags = Tag.objects.filter(post=post)
    comments = Postcomment.objects.filter(post=post, parent=None).order_by('-time_stamp')
    replies = Postcomment.objects.filter(post=post).exclude(parent=None).order_by('-time_stamp')
    repDict = {}
    year_ago = datetime.date.today()-datetime.timedelta(days=365)
    popular = Post.objects.filter(time_stamp__gte=year_ago).order_by('-views').order_by('-time_stamp')
    for reply in replies:
        if reply.parent.serial_no not in repDict.keys():
            repDict[reply.parent.serial_no] = [reply]
        else:
            repDict[reply.parent.serial_no].append(reply)
    context = {
        'post': post,
        'comments':comments, 
        'replies':repDict, 
        'popular':popular, 
        'latest':recent_post, 
        'tags':tags,
        'user':request.user
        }
    return render(request, 'blog/blogpost.html', context)

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        post_serial_no = request.POST.get('postSno')
        post = Post.objects.get(serial_no=post_serial_no)
        parent_serial_no = request.POST.get('parent_Sno')
        
        if parent_serial_no == "" :
            if comment == "":
                messages.error(request, "Please enter a comment.")
            else:
                comment = Postcomment(comment=comment, user=user, post=post)
                comment.save()
                messages.success(request, "You have successfully commented on this post.")
        else:
            if comment == "":
                messages.error(request, "Please enter a reply.")
            else:
                parent = Postcomment.objects.get(serial_no=parent_serial_no)
                comment = Postcomment(comment=comment, user=user, post=post, parent=parent)
                comment.save()
                messages.success(request, "You have successfully replied to this comment.")
    return redirect(f"/blog/{post.slug}") 
