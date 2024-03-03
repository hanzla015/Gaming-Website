from django.urls import path
from home import views

# Urls here
urlpatterns = [
    path('', views.home, name='home'),
    path('playlist/', views.playlists, name='videos'),
    path('contact/', views.contacts, name='contact'),
    path('changepass/', views.changePass, name='changepassword'),
    path('search/', views.search, name='search'),
    path('signup', views.register, name='signup'),
    path('login', views.loginuser, name='login'),
    path('logout', views.logoutuser, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('account-activation', views.otp_verifier, name='account-activation'),
    path('resend_otp', views.resend_otp),
    path('playlist/<str:slug>/', views.videos, name="video"),
    path('playlist/<str:slug>/video', views.vid_prev, name="videos"),
    path('pops', views.native, name="Ads"),
    
]
