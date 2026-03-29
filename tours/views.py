from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.db.models import Q, Prefetch
from .models import (
    Tour, TourCategory, TourImage, IncludedItem, ExcludedItem,
    TourNote, ItemToBring, ItineraryItem, TourAvailability,
    CancellationPolicyRule, PickupLocation
)


class TourListView(ListView):
    """
    Display list of all active tours with filtering and search capabilities
    """
    model = Tour
    template_name = 'tours/tour_list.html'
    context_object_name = 'tours'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Tour.objects.filter(is_active=True).select_related().prefetch_related(
            Prefetch('images', queryset=TourImage.objects.filter(is_main=True)),
            'categories',
            'languages'
        )
        
        # Search functionality
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(short_description__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Category filter
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
        
        # Difficulty filter
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Experience type filter
        experience_type = self.request.GET.get('experience_type')
        if experience_type:
            queryset = queryset.filter(experience_type=experience_type)
        
        # Sorting
        sort_by = self.request.GET.get('sort', '-is_featured')
        valid_sorts = {
            'newest': '-created_at',
            'popular': '-review_count',
            'rating': '-rating_average',
            'title': 'title',
            'featured': '-is_featured',
        }
        queryset = queryset.order_by(valid_sorts.get(sort_by, '-is_featured'), '-created_at')
        
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = TourCategory.objects.all()
        context['difficulty_choices'] = Tour.DIFFICULTY_CHOICES
        context['experience_type_choices'] = Tour.EXPERIENCE_TYPE_CHOICES
        context['current_category'] = self.request.GET.get('category', '')
        context['current_difficulty'] = self.request.GET.get('difficulty', '')
        context['current_experience_type'] = self.request.GET.get('experience_type', '')
        context['search_query'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', 'featured')
        return context


class TourDetailView(DetailView):
    """
    Display detailed information about a specific tour
    Optimized with prefetch_related to minimize database queries
    """
    model = Tour
    template_name = 'tours/tour_detail.html'
    context_object_name = 'tour'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        # Optimize queries with prefetch_related
        return Tour.objects.filter(is_active=True).prefetch_related(
            'images',
            'categories',
            'languages',
            'accessibility_options',
            'included_items',
            'excluded_items',
            'notes',
            'items_to_bring',
            'itinerary_items',
            'pickup_locations',
            'cancellation_rules',
            Prefetch(
                'availabilities',
                queryset=TourAvailability.objects.filter(
                    date__gte=timezone.now().date(),
                    is_available=True
                ).order_by('date', 'start_time')  # All available dates
            )
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tour = self.object
        
        # Organize images
        images = list(tour.images.all())
        context['main_image'] = next((img for img in images if img.is_main), images[0] if images else None)
        context['gallery_images'] = [img for img in images if not img.is_main] if images else []
        
        # Organize included and excluded items
        context['included_items'] = tour.included_items.all()
        context['excluded_items'] = tour.excluded_items.all()
        
        # Organize notes by type
        notes = tour.notes.all()
        context['general_notes'] = [n for n in notes if n.note_type == 'general']
        context['restrictions'] = [n for n in notes if n.note_type == 'restriction']
        context['important_notes'] = [n for n in notes if n.note_type == 'important']
        context['all_notes'] = notes
        
        # Items to bring (separated by required/recommended)
        items_to_bring = tour.items_to_bring.all()
        context['required_items'] = [item for item in items_to_bring if item.is_required]
        context['recommended_items'] = [item for item in items_to_bring if not item.is_required]
        
        # Itinerary
        context['itinerary_items'] = tour.itinerary_items.all()
        
        # Pickup locations
        pickup_locations = tour.pickup_locations.all()
        context['primary_pickup'] = next((loc for loc in pickup_locations if loc.is_primary), None)
        context['additional_pickups'] = [loc for loc in pickup_locations if not loc.is_primary]
        context['all_pickup_locations'] = pickup_locations
        
        # Cancellation policy
        context['cancellation_rules'] = tour.cancellation_rules.all()
        
        # Availability (prepared for booking integration) - limit to next 30 dates
        context['available_dates'] = list(tour.availabilities.all())[:30]
        
        # Related/similar tours (optional, based on categories)
        if tour.categories.exists():
            context['related_tours'] = Tour.objects.filter(
                is_active=True,
                categories__in=tour.categories.all()
            ).exclude(pk=tour.pk).distinct().prefetch_related(
                Prefetch('images', queryset=TourImage.objects.filter(is_main=True))
            )[:4]
        else:
            context['related_tours'] = Tour.objects.filter(
                is_active=True
            ).exclude(pk=tour.pk).prefetch_related(
                Prefetch('images', queryset=TourImage.objects.filter(is_main=True))
            )[:4]
        
        # Prepare participant types for booking UI (future integration with bookings app)
        # The bookings app will use this structure to build the booking form
        context['participant_types'] = [
            {'code': 'adult', 'label': 'Adult', 'description': 'Age 13+'},
            {'code': 'child', 'label': 'Child', 'description': 'Age 4-12'},
            {'code': 'infant', 'label': 'Infant', 'description': 'Age 0-3'},
        ]
        
        return context


# Additional utility views can be added here as needed
# For example:
# - Featured tours for homepage
# - Tours by category
# - Search results
# - AJAX endpoints for availability checking (future integration with bookings app)

def featured_tours_view(request):
    """
    Display featured tours (can be used on homepage or landing pages)
    """
    featured_tours = Tour.objects.filter(
        is_active=True,
        is_featured=True
    ).prefetch_related(
        Prefetch('images', queryset=TourImage.objects.filter(is_main=True)),
        'categories'
    )[:6]
    
    context = {
        'featured_tours': featured_tours,
    }
    
    return render(request, 'tours/featured_tours.html', context)
