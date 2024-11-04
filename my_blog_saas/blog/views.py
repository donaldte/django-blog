import json
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from .models import Post, Tag, Category
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.select_related('author', 'category').prefetch_related('tags').filter(is_published=True)
        
        # Full-text search with PostgreSQL
        query = request.GET.get('q')
        if query:
            # Define search vector and query
            search_vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')
            search_query = SearchQuery(query)

            # Annotate posts with rank based on search
            posts = (
                Post.objects.annotate(rank=SearchRank(search_vector, search_query))
                .filter(rank__gte=0.1)  # Adjust threshold as needed
                .select_related('author', 'category')
                .prefetch_related('tags')
                .order_by('-rank')  # Order by relevance
            )
            messages.success(request, f'Search results for: {query}')

        # Fetch all tags and latest blogs
        tags = Tag.objects.all()
        latest_blogs = posts.order_by('-created')[:4]

        # Paginate posts - 6 posts per page
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'posts': page_obj,
            'tags': tags,
            'latest_blogs': latest_blogs,
        }
        return render(request, 'pages/home.html', context)

    

home_view = HomeView.as_view()    
    
class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/about.html')
    
about_view = AboutView.as_view()  


class DetailBlogView(View):
    def get(self, request, pk=None, *args, **kwargs):
        
        post = get_object_or_404(Post, pk=pk)
        categories = Category.objects.all()
        popular_posts = Post.objects.order_by('-views_count')[:4]
        newest_posts = Post.objects.order_by('-created')[:4]
        
        context = {
            'post': post,
            'categories': categories,
            'popular_posts': popular_posts,
            'instagram_posts': newest_posts
        }
        return render(request, 'pages/blog_detail.html', context)  
    
detail_blog_view = DetailBlogView.as_view()    




@csrf_exempt
@login_required
def update_profile_ajax(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        bio = data.get("bio")
        location = data.get("location")
        website = data.get("website")
        
        # Update the user's profile
        profile = request.user.profile
        profile.bio = bio
        profile.location = location
        profile.website = website
        profile.save()

        return JsonResponse({"success": True, "message": "Profile updated successfully!"})
    return JsonResponse({"success": False, "message": "Invalid request"})
