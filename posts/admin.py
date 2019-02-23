from django.contrib import admin
from .models import Post
from .models import HashTag

admin.site.register(Post)
admin.site.register(HashTag)
