from django.contrib import admin
from home.models import *

# Register your models here.
class VideoAdmin(admin.TabularInline):
    model = Video

class PlaylistAdmin(admin.ModelAdmin):
    inlines = [VideoAdmin]

class TagAdmin(admin.TabularInline):
    model = Tag

admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Contact)
admin.site.register(HeroImage)
admin.site.register(Userdetail)
admin.site.register(OTP)
admin.site.register(Videocomment)
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    inlines = [TagAdmin]
    class Media:
        js= ('tinyinject.js',)
