from django.shortcuts import render, redirect, HttpResponse
from home.models import *
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User 
import datetime
from django.http import JsonResponse
from home.templatetags import extras
import random
from drhanzlaffweb import settings
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
import requests
from django.contrib.auth.decorators import login_required
from blog.models import *
from django.contrib import messages 
import json
# Html email required stuff
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.
def home(request):
    images = HeroImage.objects.filter(publish=True)
    params = {
        'images' : images
    }
    return render(request, 'home/home.html', params)

def playlists(request):
    all_vid = Playlist.objects.filter(publish=True)
    print(all_vid)
    params = {
        'all_vid':all_vid,
            }
    return render(request, 'home/playlist.html', params)

def videos(request, slug):
    playlist = Playlist.objects.get(slug=slug)
    serial_no = request.GET.get('video')
    videos = playlist.video_set.all().order_by("serial_no")
    # video1 = Video.objects.get(serial_no=serial_no, playlist=playlist)
    # vid_title = (video1.Title)
    # tags = Tag.objects.filter(video_ref=vid_title)
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        video_serial_no = request.POST.get('videoSno')
        video = Video.objects.get(serial_no=video_serial_no, playlist=playlist)
        parent_serial_no = request.POST.get('parent_Sno')
        if parent_serial_no == "" :
            if comment == "":
                pass
            else:
                comment = Videocomment(comment=comment, user=user, video=video)
                comment.save()
        else:
            if comment=="":
                pass
            else:
                parent = Videocomment.objects.get(serial_no=parent_serial_no)
                comment = Videocomment(comment=comment, user=user, video=video, parent=parent)
                comment.save()
    next_vid = 2
    prev_vid = None
    if serial_no is None:
        serial_no = 1
    else:
        next_vid = int(serial_no) + 1
        if len(videos) < next_vid:
            next_vid = None
        prev_vid = int(serial_no) - 1
    video = Video.objects.get(serial_no=serial_no, playlist=playlist)
    # handling comments
    comments = Videocomment.objects.filter(video=video, parent=None).order_by('-time_stamp')
    replies = Videocomment.objects.filter(video=video).exclude(parent=None).order_by('-time_stamp')
    repDict = {}
    for reply in replies:
        if reply.parent.serial_no not in repDict.keys():
            repDict[reply.parent.serial_no] = [reply]
        else:
            repDict[reply.parent.serial_no].append(reply)
    params = {
        'playlist':playlist,
        'video':video,
        "videos":videos,
        'next_vid':next_vid,
        'prev_vid':prev_vid,
        'comments':comments,
        'replies':repDict,
        }
    if request.is_ajax():
        if request.method == "POST":
            sno = request.POST.get('videoSno')
        video = Video.objects.get(serial_no=sno, playlist=playlist)
        # handling comments
        vid_comments = Videocomment.objects.filter(video=video, parent=None).order_by('-time_stamp')
        vid_replies = Videocomment.objects.filter(video=video).exclude(parent=None).order_by('-time_stamp')
        vid_repDict = {}
        for reply in vid_replies:
            if reply.parent.serial_no not in vid_repDict.keys():
                vid_repDict[reply.parent.serial_no] = [reply]
            else:
                vid_repDict[reply.parent.serial_no].append(reply)
        context = {
        'playlist':playlist,
        'video':video,
        "videos":videos,
        'next_vid':next_vid,
        'prev_vid':prev_vid,
        'comments':vid_comments,
        'replies':vid_repDict,
        }
        html = render_to_string('home/comment.html', context, request)
        return JsonResponse({'form':html})
    return render(request, 'home/video.html', params)

def vid_prev(request, slug):
    playlist = Playlist.objects.get(slug=slug)
    videos = playlist.video_set.all().order_by("serial_no")
    params = {
        'playlist':playlist,
        "videos":videos,
        }
    return render(request, 'home/vid_prev.html', params)

def contacts(request):
    if request.method =="POST":
        first_name = request.POST.get('firstName', '')
        last_name = request.POST.get('lastName', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')

        # recaptcha validation and sending
        clientkey = request.POST['g-recaptcha-response']
        secretkey = '6LcrviYeAAAAAMSUoiLlFntbxZ6niAzGDzOXdOVc'
        captchadata = {
            'secret': secretkey,
            'response':clientkey
                        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchadata)
        response = json.loads(r.text)
        verify = response['success']
        if verify:
            contact = Contact(first_name=first_name, last_name=last_name, email=email, phone=phone, content=desc)
            contact.save()
            messages.success(request, "Your message has been sent.")
            return render(request, 'home/contact.html')
        else:
            return render(request, 'home/contact.html')
    return render(request,'home/contact.html')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == "POST":
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        phone = request.POST['phone']
        user = User.objects.filter(username=request.user).update(first_name=first_name, last_name=last_name)
        user_info = Userdetail.objects.filter(username=request.user)
        user_info.update(first_name=first_name, last_name=last_name, phone=phone)
        messages.success(request, "Your profile has been updated successfully.")
        return redirect('/profile')
    return render(request, 'home/profile.html')

# Managing Authentications and Resending Otps
def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        # get the post parameters
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['email']
        username = request.POST['userName']
        password_1 = request.POST['password1']
        password_2 = request.POST['password2']
        phone = request.POST['phone']
        # Check for errors in input
        if User.objects.filter(username = username).first():
            messages.error(request, "This username is already taken")
            return redirect('/signup')

        elif User.objects.filter(email = email).first():
            messages.error(request, "An account with this email already exists please try another.")
            return redirect('/signup')

        # Create the user
        else:
            # creating user and saving it
            myuser = User.objects.create_user(username, email, password_1)
            myuser.is_active = False
            myuser.first_name = first_name
            myuser.last_name = last_name
            userinfo = Userdetail(user=User.objects.filter(username=username).first(), username=username, first_name=first_name, last_name=last_name, phone=phone)
            userinfo.save()
            myuser.save()
            # MAnaging OTP and sending
            usr = User.objects.get(username=username)
            otp = random.randint(100000, 999999)
            user_otp = OTP(username=User.objects.get(username=username), otp=otp)
            user_otp.save()
            # Html email start here
            greeting = f"Hello {first_name} {last_name}!"
            content = f"Your account has been created successfully on DR HANZLA FF. Use this Otp to verify your account. This is a secret key. Don't share this key with anyone. In case of any problem contact the DR HANZLA FF admin on our website.\nThanks!"
            context = {'greeting':greeting, 'content':content, 'otp':otp}
            html_content = render_to_string("home/email.html", context)
            text_content = strip_tags(html_content)
            send_email = EmailMultiAlternatives(
                "Welcome to DR HANZLA FF - Verify Your account",
                text_content,
                settings.EMAIL_HOST_USER,
                [email],
                )
            send_email.attach_alternative(html_content, "text/html")
            send_email.send(fail_silently=False)
        return render(request, "home/signup.html", {'otp':True, 'user':usr})
    return render(request, 'home/signup.html')
    
def loginuser(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        login_username = request.POST['loginUsername']
        login_password = request.POST['login-Password']
        try:
            user_email = User.objects.get(email=login_username)
            login_username = user_email
            user = authenticate(username=login_username, password=login_password)
        except:
            user = authenticate(username=login_username, password=login_password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in to DR HANZLA FF.")
            return redirect('/')

        elif not User.objects.filter(username=login_username).exists():
            messages.error(request, "There's no account exists for the given information.")
            return redirect('/login')
        
        elif not User.objects.get(username=login_username).is_active:
            usr = User.objects.get(username=login_username)
            otp = random.randint(100000, 999999)
            user_otp = OTP(username=User.objects.get(username=login_username), otp=otp)
            user_otp.save()
            # Html email start here
            greeting = f"Hello {usr.first_name} {usr.last_name}!"
            content = f"Your account is created successfully on DR HANZLA FF. Use this Otp to verify your account. This is a secret key. Don't share this key with anyother. In case of any problem contact the DR HANZLA FF admin.\nThanks!"
            context = {'greeting':greeting, 'content':content, 'otp':otp}
            html_content = render_to_string("home/email.html", context)
            text_content = strip_tags(html_content)
            send_email = EmailMultiAlternatives(
                "Welcome to DR HANZLA FF - Verify Your account",
                text_content,
                settings.EMAIL_HOST_USER,
                [usr.email],
                )
            send_email.attach_alternative(html_content, "text/html")
            send_email.send(fail_silently=False)
            return render(request, "home/login.html", {'otp':True, 'user':usr})
            
        else:
            messages.error(request, "Invalid credential, please try again.")
            return render(request, 'home/login.html')
    return render(request, "home/login.html")

def logoutuser(request):
    if request.user.is_authenticated:
        url = request.META.get('HTTP_REFERER')
        logout(request)
        messages.success(request, "You have succesfully logged Out.")
        return redirect(url)
    else:
        return redirect('/login')

def otp_verifier(request):
    if request.method == "POST":
        get_otp = request.POST['otp']
        if get_otp:
            username = request.POST['user']
            usr = User.objects.get(username=username)
            my_user = User.objects.get(username=username)
            if int(get_otp) == OTP.objects.filter(username=usr).last().otp:
                my_user.is_active = True
                my_user.save()
                messages.success(request, "Your account is verified successfully.")
                return redirect('/login')
            else:
                messages.error(request, "The OTP you have entered is not correct.")
                return render(request, 'home/signup.html', {'otp':True, 'user':usr}) 
    return redirect('/')

def resend_otp(request):
    if request.method == "GET":
        user = request.GET['user']
        if User.objects.filter(username=user).exists() and not User.objects.get(username=user).is_active:
            usr = User.objects.get(username=user)
            otp = random.randint(100000, 999999)
            user_otp = OTP(username=User.objects.get(username=user), otp=otp)
            user_otp.save()
            # Html email start here
            greeting = f"Hello {usr.first_name} {usr.last_name}!"
            content = f"Your account is created successfully on DR HANZLA FF. Use this Otp to verify your account. This is a secret key. Don't share this key with anyother. In case of any problem contact the DR HANZLA FF admin on our website.\nThanks!"
            context = {'greeting':greeting, 'content':content, 'otp':otp}
            html_content = render_to_string("home/email.html", context)
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                "Welcome to DR HANZLA FF - Verify Your account",
                text_content,
                settings.EMAIL_HOST_USER,
                [usr.email],
                )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)
            return HttpResponse("Resend")
    return HttpResponse("Can't Send ")

def changePass(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                v = form.save()
                update_session_auth_hash(request, v)
                messages.success(request, "Your Password has been changed successfully.")
                return redirect('/')
        else:
            form = PasswordChangeForm(request.user)
        params = {
            'form':form,
        }
        return render(request, 'home/changepass.html', params)
    else:
        return redirect('/login')

def search(request):
    query = request.GET['query']
    if len(query) > 150:
        all_posts = Post.objects.none()
        all_playlists = Playlist.objects.none()
        all_videos = Video.objects.none()
        messages.warning(request, 'Your query does not match any result.')
    elif len(query) == 0:
        latest_blogs = Post.objects.all().order_by('-time_stamp')
        latest_playlists = Playlist.objects.all().order_by('-time_stamp')
        latest_videos = Video.objects.all().order_by('-time_stamp')
        all_posts = latest_blogs
        all_playlists = latest_playlists
        all_videos = latest_videos
    else:
        all_video_title = Video.objects.filter(Title__icontains=query)
        all_video_content = Video.objects.filter(content__icontains=query)
        all_post_title = Post.objects.filter(title__icontains=query)
        all_post_content = Post.objects.filter(content__icontains=query)
        all_playlist_title = Playlist.objects.filter(name__icontains=query)
        all_playlist_content = Playlist.objects.filter(description__icontains=query)
        all_posts = all_post_title.union(all_post_content)
        all_videos = all_video_title.union(all_video_content)
        all_playlists = all_playlist_title.union(all_playlist_content)
    if (all_posts.count() == 0) and( all_playlists.count() == 0) and (all_videos.count() == 0):
        messages.warning(request, 'No search result found for your query.')
    params = {'allposts':all_posts, 'allplaylists':all_playlists, 'all_videos':all_videos, 'query':query}
    return render(request, 'home/search.html', params)

def native(request):
    return render (request, 'home/pops.html')