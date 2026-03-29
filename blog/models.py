from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from ckeditor.fields import RichTextField
import math

User = get_user_model()


class Category(models.Model):
    """
    Blog post categories (e.g., Travel Tips, Destinations, Culture, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='blog/categories/', blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")
        ordering = ['display_order', 'name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'slug': self.slug})
    
    @property
    def post_count(self):
        """Return count of published posts in this category"""
        return self.posts.filter(status='published', published_at__lte=timezone.now()).count()


class Post(models.Model):
    """
    Blog post model with full SEO support and multilingual content
    """
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('published', _('Published')),
        ('archived', _('Archived')),
    ]
    
    SCHEMA_TYPE_CHOICES = [
        ('Article', 'Article'),
        ('BlogPosting', 'BlogPosting'),
        ('NewsArticle', 'NewsArticle'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200, help_text="Post title")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    featured_image = models.ImageField(
        upload_to='blog/posts/%Y/%m/',
        blank=True,
        null=True,
        help_text="Main image for the post"
    )
    excerpt = models.TextField(
        max_length=500,
        blank=True,
        help_text="Short description/summary of the post"
    )
    content = RichTextField(help_text="Main content (supports rich text editing)")
    
    # Relationships
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='blog_posts'
    )
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated tags (e.g., travel, europe, adventure)"
    )
    
    # Status and Features
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Feature this post on homepage or listings"
    )
    
    # Engagement
    view_count = models.PositiveIntegerField(default=0, editable=False)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date and time when the post should be published"
    )
    
    # SEO Fields
    meta_title = models.CharField(
        max_length=60,
        blank=True,
        help_text="SEO title (leave blank to use post title)"
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="SEO meta description (recommended 150-160 characters)"
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="SEO keywords, comma-separated"
    )
    canonical_url = models.URLField(
        blank=True,
        help_text="Canonical URL if different from default"
    )
    
    # Open Graph (Social Media)
    og_title = models.CharField(
        max_length=60,
        blank=True,
        help_text="Open Graph title (leave blank to use meta title or post title)"
    )
    og_description = models.CharField(
        max_length=200,
        blank=True,
        help_text="Open Graph description"
    )
    og_image = models.ImageField(
        upload_to='blog/og_images/%Y/%m/',
        blank=True,
        null=True,
        help_text="Open Graph image (leave blank to use featured image)"
    )
    
    # Schema.org
    schema_type = models.CharField(
        max_length=20,
        choices=SCHEMA_TYPE_CHOICES,
        default='BlogPosting',
        help_text="Schema.org type for structured data"
    )
    
    class Meta:
        verbose_name = _("Blog Post")
        verbose_name_plural = _("Blog Posts")
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['status']),
            models.Index(fields=['slug']),
        ]
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure unique slug
            original_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        # Auto-set published_at when status changes to published
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    @property
    def is_published(self):
        """Check if post is published and publish date has passed"""
        return (
            self.status == 'published' and 
            self.published_at and 
            self.published_at <= timezone.now()
        )
    
    @property
    def reading_time(self):
        """Calculate estimated reading time in minutes"""
        # Average reading speed: 200 words per minute
        from django.utils.html import strip_tags
        word_count = len(strip_tags(self.content).split())
        minutes = math.ceil(word_count / 200)
        return max(1, minutes)  # At least 1 minute
    
    @property
    def tag_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []
    
    def get_related_posts(self, limit=3):
        """Get related posts based on category and tags"""
        related = Post.objects.filter(
            status='published',
            published_at__lte=timezone.now()
        ).exclude(pk=self.pk)
        
        # Prioritize same category
        if self.category:
            related = related.filter(category=self.category)
        
        return related.order_by('-published_at')[:limit]
    
    def increment_view_count(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    # SEO Helper Methods
    def get_meta_title(self):
        """Return meta title or fall back to post title"""
        return self.meta_title or self.title
    
    def get_meta_description(self):
        """Return meta description or fall back to excerpt"""
        return self.meta_description or self.excerpt
    
    def get_og_title(self):
        """Return OG title with fallbacks"""
        return self.og_title or self.meta_title or self.title
    
    def get_og_description(self):
        """Return OG description with fallbacks"""
        return self.og_description or self.meta_description or self.excerpt
    
    def get_og_image_url(self):
        """Return OG image URL with fallback to featured image"""
        if self.og_image:
            return self.og_image.url
        elif self.featured_image:
            return self.featured_image.url
        return None
