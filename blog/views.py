from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from django.utils import timezone
from .models import Post, Category


class PostListView(ListView):
    """
    Display list of published blog posts with search and filtering
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9  # 9 posts per page (3x3 grid)
    
    def get_queryset(self):
        """Get published posts with optional search and filtering"""
        queryset = Post.objects.filter(
            status='published',
            published_at__lte=timezone.now()
        ).select_related('category', 'author').order_by('-published_at')
        
        # Search functionality
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(excerpt__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tags__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all active categories with post counts
        context['categories'] = Category.objects.filter(
            is_active=True
        ).annotate(
            published_post_count=Count('posts', filter=Q(
                posts__status='published',
                posts__published_at__lte=timezone.now()
            ))
        ).order_by('display_order', 'name')
        
        # Get featured posts (max 3)
        context['featured_posts'] = Post.objects.filter(
            status='published',
            published_at__lte=timezone.now(),
            is_featured=True
        ).select_related('category', 'author').order_by('-published_at')[:3]
        
        # Get recent posts for sidebar (max 5)
        context['recent_posts'] = Post.objects.filter(
            status='published',
            published_at__lte=timezone.now()
        ).select_related('category').order_by('-published_at')[:5]
        
        # Pass search query back to template
        context['search_query'] = self.request.GET.get('q', '')
        
        return context


class CategoryPostListView(ListView):
    """
    Display posts filtered by category
    """
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        """Get published posts for specific category"""
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'], is_active=True)
        
        queryset = Post.objects.filter(
            status='published',
            published_at__lte=timezone.now(),
            category=self.category
        ).select_related('category', 'author').order_by('-published_at')
        
        # Search within category
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(excerpt__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tags__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        
        # Get all active categories
        context['categories'] = Category.objects.filter(
            is_active=True
        ).annotate(
            published_post_count=Count('posts', filter=Q(
                posts__status='published',
                posts__published_at__lte=timezone.now()
            ))
        ).order_by('display_order', 'name')
        
        # Get recent posts for sidebar
        context['recent_posts'] = Post.objects.filter(
            status='published',
            published_at__lte=timezone.now()
        ).select_related('category').order_by('-published_at')[:5]
        
        context['search_query'] = self.request.GET.get('q', '')
        
        return context


class PostDetailView(DetailView):
    """
    Display individual blog post
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        """Only allow published posts"""
        return Post.objects.filter(
            status='published',
            published_at__lte=timezone.now()
        ).select_related('category', 'author')
    
    def get_object(self, queryset=None):
        """Get post and increment view count"""
        obj = super().get_object(queryset)
        
        # Increment view count (avoid counting repeated views in same session)
        session_key = f'viewed_post_{obj.pk}'
        if not self.request.session.get(session_key, False):
            obj.increment_view_count()
            self.request.session[session_key] = True
        
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get related posts
        context['related_posts'] = self.object.get_related_posts(limit=3)
        
        # Get recent posts for sidebar
        context['recent_posts'] = Post.objects.filter(
            status='published',
            published_at__lte=timezone.now()
        ).exclude(pk=self.object.pk).select_related('category').order_by('-published_at')[:5]
        
        # Get all active categories for sidebar
        context['categories'] = Category.objects.filter(
            is_active=True
        ).annotate(
            published_post_count=Count('posts', filter=Q(
                posts__status='published',
                posts__published_at__lte=timezone.now()
            ))
        ).order_by('display_order', 'name')
        
        return context
