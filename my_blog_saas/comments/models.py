from django.db import models
from django.contrib.auth import get_user_model
from my_blog_saas.blog.models import Post
from my_blog_saas.users.models import AbstractBaseModel

User = get_user_model()


class Comment(AbstractBaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"
