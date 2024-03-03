from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
class HeroImage(models.Model):
    hero_thumbnail_link = models.CharField(max_length=500, default="", null=False)
    game_card_thumbnail_link = models.CharField(max_length=500, default="", null=False)
    blog_card_thumbnail_link = models.CharField(max_length=500, default="", null=False)
    publish = models.BooleanField(default=False)

class Playlist(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=300, blank=True)
    thumbnail_link = models.CharField(max_length=600, null=True, default='')
    publish = models.BooleanField(default=False)
    time_stamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.name

class Contact(models.Model):
    serial_no = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=100, default="")
    email = models.EmailField(max_length=100, default="")
    content = models.TextField()
    time_stamp = models.TimeField(auto_now_add=True)

    def __str__(self):
        return 'Message From'+f'{self.first_name}{self.last_name} - {self.email}'

class Userdetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=60, default="")
    first_name = models.CharField(max_length=60, default="")
    last_name = models.CharField(max_length=60, default="")
    phone = models.CharField(max_length=40, null=True)

    def __str__(self):
        return self.username+"'s "+" detail"

class OTP(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField(blank=True)
    time_stamp = models.DateTimeField(auto_now=True)

class Video(models.Model):
    serial_no = models.IntegerField(null=False)
    Title = models.CharField(max_length=200, null=False, blank=True)
    playlist = models.ForeignKey(Playlist, null=False, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=100, null=False, blank=True)
    is_preview = models.BooleanField(default=False)
    content = models.TextField(null=True)
    thumbnail_link = models.CharField(max_length=1000, null=False, default="")
    time_stamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.Title[0:50]+"......"

class Videocomment(models.Model):
    serial_no = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    time_stamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:15] +"....."+" by " + self.user.username

class Tag(models.Model):
    tag = models.CharField(max_length=70, null=False, blank=True)
    video_ref = models.ForeignKey(Video, null=False, on_delete=models.CASCADE)
