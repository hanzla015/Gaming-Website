from django.contrib import admin
from blog.models import *
# Register your models here.
class TagAdmin(admin.TabularInline):
    model = Tag

admin.site.register(Postcomment)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [TagAdmin]
    class Media:
        js= ('tinyinject.js',)