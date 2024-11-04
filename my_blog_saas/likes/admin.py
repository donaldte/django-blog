from django.contrib import admin

from .models import Like

class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created']
    search_fields = ['user', 'post']
    list_per_page = 20  
    
    
admin.site.register(Like, LikeAdmin)