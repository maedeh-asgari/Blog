from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft' # name:DRAFT value:DF label:Draft
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='published_at')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='author_posts')
    body = models.TextField()
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    
    objects = models.Manager() #defualt
    published = PublishedManager() #custom

    tags = TaggableManager()

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at']),
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.published_at.year,
                             self.published_at.month,
                             self.published_at.day,
                             self.slug])
    

class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='post_comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    