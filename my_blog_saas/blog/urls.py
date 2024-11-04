from my_blog_saas.blog.views import home_view, about_view, detail_blog_view, update_profile_ajax
from django.urls import path

app_name = "blog"

urlpatterns = [
    path("", home_view, name="home"),
    path("about/", about_view, name="about"),
    path("blog/<str:pk>/", detail_blog_view, name="blog_detail"),
        path('profile/update/', update_profile_ajax, name='update_profile_ajax'),

]
