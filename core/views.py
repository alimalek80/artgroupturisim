from django.shortcuts import render
from django.db.models import Prefetch
from tours.models import Tour, TourImage


def home_view(request):
    """
    Homepage view displaying welcome content and featured tours.
    """
    # Get featured and active tours with their main images
    featured_tours = Tour.objects.filter(
        is_active=True,
        is_featured=True
    ).prefetch_related(
        Prefetch('images', queryset=TourImage.objects.filter(is_main=True)),
        'categories'
    ).order_by('-created_at')[:8]
    
    # If not enough featured tours, get regular active tours
    if featured_tours.count() < 8:
        additional_tours = Tour.objects.filter(
            is_active=True
        ).exclude(
            id__in=[tour.id for tour in featured_tours]
        ).prefetch_related(
            Prefetch('images', queryset=TourImage.objects.filter(is_main=True)),
            'categories'
        ).order_by('-created_at')[:8 - featured_tours.count()]
        
        tours = list(featured_tours) + list(additional_tours)
    else:
        tours = list(featured_tours)
    
    context = {
        'page_title': 'Welcome to Art Tourism',
        'tours': tours,
    }
    return render(request, 'core/home.html', context)
