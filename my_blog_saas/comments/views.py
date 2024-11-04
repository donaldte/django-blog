# views.py

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Comment, Post

@login_required
@require_POST
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content')
    parent_id = request.POST.get('parent_id')
    parent = Comment.objects.get(id=parent_id) if parent_id else None

    comment = Comment.objects.create(post=post, author=request.user, content=content, parent=parent)
    return JsonResponse({'success': True, 'comment_id': comment.id, 'message': 'Comment created successfully!'})

@login_required
@require_POST
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    content = request.POST.get('content')
    comment.content = content
    comment.save()
    return JsonResponse({'success': True, 'message': 'Comment updated successfully!'})

@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    comment.delete()
    return JsonResponse({'success': True, 'message': 'Comment deleted successfully!'})

@login_required
@require_POST
def reply_to_comment(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    post = parent_comment.post
    content = request.POST.get('content')

    reply = Comment.objects.create(post=post, author=request.user, content=content, parent=parent_comment)
    return JsonResponse({'success': True, 'reply_id': reply.id, 'message': 'Reply created successfully!'})
