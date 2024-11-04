import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
from .models import SubscriptionPlan
from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

stripe.api_key = settings.STRIPE_SECRET_KEY

def start_stripe_subscription(request, plan_id):
    try:
        # Retrieve the selected plan
        plan = SubscriptionPlan.objects.get(id=plan_id)
        
        # Check if a Stripe Product and Price exist for this plan type
        product_data = {
            'name': plan.name,
            'description': plan.description,
        }

        # Define interval based on plan_type
        interval = plan.plan_type

        price_data = stripe.Price.create(
            unit_amount=int(plan.price * 100),  # Stripe expects amount in cents
            currency='usd',
            recurring={"interval": interval},
            product_data=product_data,
        )

        # Create a Stripe checkout session
        success_url = request.build_absolute_uri(reverse('subscriptions:stripe_subscription_success')) + '?session_id={CHECKOUT_SESSION_ID}'
        cancel_url = request.build_absolute_uri(reverse('subscriptions:stripe_subscription_cancel'))

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='subscription',
            line_items=[{
                'price': price_data.id,
                'quantity': 1,
            }],
            customer_creation='always',
            success_url=success_url,
            cancel_url=cancel_url,
        )

        return redirect(checkout_session.url, code=303)

    except Exception as e:
        return JsonResponse({'error': str(e)})




def stripe_subscription_success(request):
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    
    if session.payment_status == 'paid':
        messages.success(request, "Subscription successful!")
        # You can activate the subscription in your system here
        return redirect('home')  # Redirect to an appropriate page

    return render(request, 'subscriptions/success.html', {'session': session})

def stripe_subscription_cancel(request):
    messages.warning(request, "Subscription was cancelled.")
    return redirect('home')  # Redirect to an appropriate page



@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET
        )

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            # Handle subscription activation here based on session data

        elif event['type'] == 'invoice.payment_failed':
            subscription_id = event['data']['object']['subscription']
            # Mark subscription as inactive in your system
            
        elif event['type'] == 'customer.subscription.deleted':
            subscription_id = event['data']['object']['id']
            # Mark subscription as canceled in your system

    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    return HttpResponse(status=200)
