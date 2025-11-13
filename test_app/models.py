from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    pages = models.PositiveSmallIntegerField(default=0)


    def __str__(self):
        return f"Book '{self.title}' -- Author: '{self.author}'"

    class Meta:
        db_table = 'books'
        ordering = ('published_date',)
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

        get_latest_by = 'published_date'

        default_related_name = 'books'
        unique_together = (('title', 'published_date'),)

        indexes = [
            models.Index(
                fields=['title', 'published_date'],
                name='ind_published_date',
            )
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'published_date'],
                name='unq_published_date'
            ),
            models.CheckConstraint(
                check=models.Q(pages__gte=0),
                name='check_pages_constraint'
            )
        ]



class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(null=True, blank=True)

class UserProfile(models.Model):
    nickname = models.CharField(max_length=120, unique=True)
    bio = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True, max_length=250)
    age = models.IntegerField()
    followers_count = models.PositiveBigIntegerField()
    posts_count = models.PositiveIntegerField()
    comments_count = models.PositiveIntegerField()
    engagement_rate = models.FloatField()

    class Meta:
        db_table = 'user_profiles'


    def __str__(self):
        return self.nickname