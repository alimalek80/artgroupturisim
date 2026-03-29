from django.urls import path
from .views import TourListView, TourDetailView, featured_tours_view

app_name = 'tours'

urlpatterns = [
    # Tour list page
    path('', TourListView.as_view(), name='tour_list'),
    
    # Featured tours (can be used on homepage)
    path('featured/', featured_tours_view, name='featured_tours'),
    
    # Tour detail page (must be last to avoid conflicts)
    path('<slug:slug>/', TourDetailView.as_view(), name='tour_detail'),
]
