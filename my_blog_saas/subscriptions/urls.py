from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('subscription/start/<int:plan_id>/', views.start_stripe_subscription, name='start_stripe_subscription'),
    path('subscription/success/', views.stripe_subscription_success, name='stripe_subscription_success'),
    path('subscription/cancel/', views.stripe_subscription_cancel, name='stripe_subscription_cancel'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]