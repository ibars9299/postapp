from django.contrib import admin

from post.models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('image','title', 'author', 'created_at')

    admin.site.register(Post)