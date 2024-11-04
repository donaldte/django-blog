from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created']
    search_fields = ['author', 'post']
    list_per_page = 20
    
admin.site.register(Comment, CommentAdmin)