from django.urls import path
from blog import views


# Urls Pattern starts here
urlpatterns = [
    path('postcomment', views.postComment, name='postcomment'),
    path('', views.blog, name='bloghome'),
    # path('blogpost', views.blogPost, name="blogPost"),
    path('<str:slug>/', views.blogPost, name='blogPost'),
]