from django.contrib import admin
from .models import Subscription, SubscriptionPlan

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'start_date', 'end_date', 'is_active']
    search_fields = ['user', 'plan']
    list_per_page = 20
    
    
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'plan_type', 'created']
    search_fields = ['name', 'plan_type']
    list_per_page = 20
    
    
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)