from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('create-comment/<str:post_id>/', views.create_comment, name='create_comment'),
    path('update-comment/<str:comment_id>/', views.update_comment, name='update_comment'),
    path('delete-comment/<str:comment_id>/', views.delete_comment, name='delete_comment'),
    path('reply-to-comment/<str:comment_id>/', views.reply_to_comment, name='reply_to_comment'),
]
