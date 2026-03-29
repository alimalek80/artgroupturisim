from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from modeltranslation.admin import TranslationAdmin
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    """Admin interface for blog categories with translation support"""
    list_display = ['name', 'slug', 'post_count', 'is_active', 'display_order', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'post_count']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'image')
        }),
        ('Settings', {
            'fields': ('is_active', 'display_order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def post_count(self, obj):
        """Display published post count"""
        count = obj.post_count
        return format_html('<strong>{}</strong> posts', count)
    post_count.short_description = 'Posts'


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    """Admin interface for blog posts with CKEditor and translation support"""
    list_display = [
        'title',
        'category',
        'author',
        'status_badge',
        'is_featured',
        'view_count',
        'reading_time_display',
        'published_at',
        'updated_at'
    ]
    list_filter = [
        'status',
        'is_featured',
        'category',
        'created_at',
        'published_at',
        'author'
    ]
    search_fields = [
        'title',
        'excerpt',
        'content',
        'tags',
        'meta_title',
        'meta_description',
        'meta_keywords'
    ]
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = [
        'view_count',
        'reading_time_display',
        'created_at',
        'updated_at',
        'preview_image',
        'preview_og_image'
    ]
    
    autocomplete_fields = ['author']
    
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Content', {
            'fields': (
                'title',
                'slug',
                'excerpt',
                'content',
            )
        }),
        ('Featured Image', {
            'fields': ('featured_image', 'preview_image'),
        }),
        ('Organization', {
            'fields': ('category', 'tags', 'author')
        }),
        ('Publishing', {
            'fields': (
                'status',
                'is_featured',
                'published_at',
            )
        }),
        ('Engagement Stats', {
            'fields': ('view_count', 'reading_time_display'),
            'classes': ('collapse',)
        }),
        ('SEO - Basic', {
            'fields': (
                'meta_title',
                'meta_description',
                'meta_keywords',
                'canonical_url',
            ),
            'classes': ('collapse',)
        }),
        ('SEO - Open Graph (Social Media)', {
            'fields': (
                'og_title',
                'og_description',
                'og_image',
                'preview_og_image',
            ),
            'classes': ('collapse',)
        }),
        ('SEO - Structured Data', {
            'fields': ('schema_type',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_published', 'make_draft', 'make_featured', 'remove_featured']
    
    def status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'published': '#28a745',
            'draft': '#6c757d',
            'archived': '#dc3545'
        }
        color = colors.get(obj.status, '#6c757d')
        
        # Check if actually published (date in past)
        if obj.status == 'published' and obj.published_at:
            if obj.published_at > timezone.now():
                return format_html(
                    '<span style="background: {}; color: white; padding: 3px 10px; '
                    'border-radius: 3px; font-weight: bold;">⏰ SCHEDULED</span>',
                    '#ffc107'
                )
        
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color, obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    
    def reading_time_display(self, obj):
        """Display reading time"""
        return f"{obj.reading_time} min"
    reading_time_display.short_description = 'Reading Time'
    
    def preview_image(self, obj):
        """Show preview of featured image"""
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; border-radius: 8px;"/>',
                obj.featured_image.url
            )
        return "No image"
    preview_image.short_description = 'Preview'
    
    def preview_og_image(self, obj):
        """Show preview of OG image"""
        if obj.og_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; border-radius: 8px;"/>',
                obj.og_image.url
            )
        elif obj.featured_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; border-radius: 8px;"/>'
                '<br><em>(Using featured image)</em>',
                obj.featured_image.url
            )
        return "No OG image"
    preview_og_image.short_description = 'OG Image Preview'
    
    # Admin Actions
    def make_published(self, request, queryset):
        """Bulk action to publish posts"""
        updated = 0
        for post in queryset:
            if post.status != 'published':
                post.status = 'published'
                if not post.published_at:
                    post.published_at = timezone.now()
                post.save()
                updated += 1
        self.message_user(request, f'{updated} post(s) marked as published.')
    make_published.short_description = 'Mark selected posts as published'
    
    def make_draft(self, request, queryset):
        """Bulk action to set posts to draft"""
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} post(s) marked as draft.')
    make_draft.short_description = 'Mark selected posts as draft'
    
    def make_featured(self, request, queryset):
        """Bulk action to feature posts"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} post(s) marked as featured.')
    make_featured.short_description = 'Mark selected posts as featured'
    
    def remove_featured(self, request, queryset):
        """Bulk action to unfeature posts"""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} post(s) removed from featured.')
    remove_featured.short_description = 'Remove featured from selected posts'
    
    def save_model(self, request, obj, form, change):
        """Auto-set author to current user if not set"""
        if not change and not obj.author:  # New post without author
            obj.author = request.user
        super().save_model(request, obj, form, change)
