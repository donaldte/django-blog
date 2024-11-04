from django.contrib import admin
from .models import Post, Category, Tag



class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_published', 'created']
    list_filter = ['is_published', 'category']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)} # Auto-generate slug from title
    date_hierarchy = 'created'
    list_per_page = 20
    
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 20
    


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 20
    date_hierarchy = 'created'
    
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)    
    
        