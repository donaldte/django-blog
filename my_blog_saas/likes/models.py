from django.db import models
from django.contrib.auth import get_user_model
from my_blog_saas.blog.models import Post
from my_blog_saas.users.models import AbstractBaseModel

User = get_user_model()

class Like(AbstractBaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')
        verbose_name_plural = 'Likes'
        

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"
