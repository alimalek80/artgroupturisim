from django.shortcuts import render, redirect
from django.db.models import Prefetch
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from tours.models import Tour, TourImage
from blog.models import Post
from contact.forms import ContactForm
from .models import AboutSection


def home_view(request):
    """
    Homepage view displaying welcome content and featured tours.
    Handles contact form submission.
    """
    # Handle contact form submission
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            # Save the message to database
            contact_message = contact_form.save()
            
            # Send email notification (optional)
            try:
                subject = f"New Contact Message from {contact_message.name}"
                message = f"""
New contact form submission:

Name: {contact_message.name}
Email: {contact_message.email}
Phone: {contact_message.phone or 'N/A'}

Message:
{contact_message.message}

Submitted at: {contact_message.created_at.strftime('%Y-%m-%d %H:%M:%S')}
                """
                
                # Send email to site admin
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],  # Change to your admin email
                    fail_silently=True,
                )
            except Exception as e:
                # Log error but don't fail the form submission
                print(f"Email sending failed: {e}")
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('core:home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        contact_form = ContactForm()
    
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
    
    # Get active about section
    about_section = AboutSection.objects.filter(is_active=True).first()
    
    # Get latest 3 published blog posts
    latest_posts = Post.objects.filter(
        status='published',
        published_at__lte=timezone.now()
    ).select_related('category', 'author').order_by('-published_at')[:3]
    
    context = {
        'page_title': 'Welcome to Art Tourism',
        'tours': tours,
        'about_section': about_section,
        'latest_posts': latest_posts,
        'contact_form': contact_form,
    }
    return render(request, 'core/home.html', context)


def about_view(request):
    """
    About page view displaying company information.
    """
    # Get active about section
    about_section = AboutSection.objects.filter(is_active=True).first()
    
    context = {
        'page_title': 'About Us',
        'about_section': about_section,
    }
    return render(request, 'core/about.html', context)
