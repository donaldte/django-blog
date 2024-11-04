from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from my_blog_saas.users.models import AbstractBaseModel


User = get_user_model()


class Tag(AbstractBaseModel):
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        verbose_name_plural = 'Tags'
        
    
    def __str__(self):
        return self.name


class Category(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        

    def __str__(self):
        return self.name

class Post(AbstractBaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    title = models.CharField(max_length=255)
    content = RichTextUploadingField()  # Use CKEditor with upload support
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    views_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Posts'
        ordering = ['-created']

    def __str__(self):
        return self.title
    
