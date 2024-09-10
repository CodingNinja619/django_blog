from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from faker import Faker
from django.utils.text import slugify

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DR", "Draft",
        PUBLISHED = "PB", "Published"
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager() # Default manager
    published = PublishedManager() # Custom manager that returns published objects

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    def __str__(self):
        return self.title[:50]

class PostFactory:
    fake = Faker()
    @staticmethod
    def create(title=None, body=None, author=None):
        title = title or PostFactory.fake.sentence()
        body = body or PostFactory.fake.paragraph()
        author = author or User.objects.first()
        slug = slugify(title)
        return Post.objects.create(title=title, body=body, author=author, slug=slug)
    
    @staticmethod
    def create_batch(n, **kwargs):
        return [PostFactory.create(**kwargs) for _ in range(n)]
    
class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name="comments")
    # Custom manager for related objects https://stacktuts.com/how-to-use-custom-manager-with-related-objects-in-django
    # Try it out!!!
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created"]

        indexes = [
            models.Index(fields=["created"]),
        ]

        def __str__(self):
            return f"Comment by {self.name} on {self.post}"