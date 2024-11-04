from django.db import models
from django.contrib.auth import get_user_model

from my_blog_saas.users.models import AbstractBaseModel

User = get_user_model()



class SubscriptionPlan(AbstractBaseModel):
    PLAN_CHOICES = [
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    plan_type = models.CharField(max_length=10, choices=PLAN_CHOICES, default='monthly')

    class Meta:
        verbose_name_plural = 'Subscription Plans'
        ordering = ['-created']

    def __str__(self):
        return f"{self.name} ({self.get_plan_type_display()})"
    
    



class Subscription(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Subscriptions'
        ordering = ['-created']

    def __str__(self):
        return f"{self.user.username} subscribed to {self.plan.name}"
