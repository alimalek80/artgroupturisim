from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class TourCategory(models.Model):
    """
    Categories for organizing tours (e.g., Adventure, Cultural, Food & Wine, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or emoji")
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = _("Tour Category")
        verbose_name_plural = _("Tour Categories")
        ordering = ['display_order', 'name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Language(models.Model):
    """
    Languages available for tour guides
    """
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, blank=True, help_text="ISO language code (e.g., en, es, fr)")
    
    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")
        ordering = ['name']
    
    def __str__(self):
        return self.name


class AccessibilityOption(models.Model):
    """
    Accessibility features available for tours
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name = _("Accessibility Option")
        verbose_name_plural = _("Accessibility Options")
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Tour(models.Model):
    """
    Main Tour model - represents a tour product offered by the travel agency
    """
    DIFFICULTY_CHOICES = [
        ('easy', _("Easy")),
        ('moderate', _("Moderate")),
        ('challenging', _("Challenging")),
        ('difficult', _("Difficult")),
    ]
    
    EXPERIENCE_TYPE_CHOICES = [
        ('group', _("Group Tour")),
        ('private', _("Private Tour")),
        ('semi_private', _("Semi-Private Tour")),
        ('self_guided', _("Self-Guided")),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    subtitle = models.CharField(max_length=300, blank=True, help_text="Short catchy description")
    short_description = models.TextField(max_length=500, help_text="Brief overview for listings")
    description = models.TextField(help_text="Full detailed description (supports HTML)")
    
    # Tour Characteristics
    duration_hours = models.PositiveIntegerField(default=0, help_text="Duration in hours")
    duration_minutes = models.PositiveIntegerField(
        default=0, 
        validators=[MaxValueValidator(59)],
        help_text="Additional minutes (0-59)"
    )
    duration_text = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Optional custom duration display (e.g., '2 days, 1 night')"
    )
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='easy')
    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPE_CHOICES, default='group')
    
    # Relationships
    categories = models.ManyToManyField(TourCategory, related_name='tours', blank=True)
    languages = models.ManyToManyField(Language, related_name='tours', blank=True)
    accessibility_options = models.ManyToManyField(
        AccessibilityOption, 
        related_name='tours', 
        blank=True
    )
    
    # Pickup Information
    pickup_information = models.TextField(
        blank=True,
        help_text="Details about pickup locations, times, and procedures"
    )
    
    # Itinerary
    itinerary_description = models.TextField(
        blank=True,
        help_text="General itinerary overview (detailed items can be added separately)"
    )
    
    # Booking Configuration (prepared for bookings app integration)
    max_participants = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Maximum number of participants per booking (leave blank for unlimited)"
    )
    min_participants = models.PositiveIntegerField(
        default=1,
        help_text="Minimum number of participants required"
    )
    booking_cutoff_hours = models.PositiveIntegerField(
        default=24,
        help_text="How many hours in advance booking must be made"
    )
    instant_confirmation = models.BooleanField(
        default=True,
        help_text="Whether booking is instantly confirmed"
    )
    
    # Reviews & Ratings (managed externally, read-only here)
    review_count = models.PositiveIntegerField(default=0, editable=False)
    rating_average = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        editable=False
    )
    
    # Status & Publishing
    is_active = models.BooleanField(default=True, help_text="Is tour available for booking?")
    is_featured = models.BooleanField(default=False, help_text="Feature on homepage?")
    published_date = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_description = models.CharField(
        max_length=160, 
        blank=True,
        help_text="SEO meta description"
    )
    
    class Meta:
        verbose_name = _("Tour")
        verbose_name_plural = _("Tours")
        ordering = ['-is_featured', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('tours:tour_detail', kwargs={'slug': self.slug})
    
    def get_duration_display(self):
        """Returns formatted duration string"""
        if self.duration_text:
            return self.duration_text
        
        hours = self.duration_hours
        minutes = self.duration_minutes
        
        if hours and minutes:
            return f"{hours}h {minutes}min"
        elif hours:
            return f"{hours} hour{'s' if hours > 1 else ''}"
        elif minutes:
            return f"{minutes} minutes"
        return "Duration varies"
    
    def __str__(self):
        return self.title


class TourImage(models.Model):
    """
    Images for a tour - supports multiple images with one main image
    """
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='tours/images/%Y/%m/')
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=200, blank=True, help_text="Alt text for accessibility")
    is_main = models.BooleanField(
        default=False,
        help_text="Main image displayed in listings and at top of detail page"
    )
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = _("Tour Image")
        verbose_name_plural = _("Tour Images")
        ordering = ['-is_main', 'display_order']
    
    def save(self, *args, **kwargs):
        # Ensure only one main image per tour
        if self.is_main:
            TourImage.objects.filter(tour=self.tour, is_main=True).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.tour.title} - Image {self.display_order}"


class IncludedItem(models.Model):
    """
    Items/services included in the tour price
    """
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='included_items')
    item = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or emoji")
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = _("Included Item")
        verbose_name_plural = _("Included Items")
        ordering = ['display_order']
    
    def __str__(self):
        return f"{self.tour.title} - Includes: {self.item}"


class ExcludedItem(models.Model):
    """
    Items/services NOT included in the tour price
    """
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='excluded_items')
    item = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or emoji")
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = _("Excluded Item")
        verbose_name_plural = _("Excluded Items")
        ordering = ['display_order']
    
    def __str__(self):
        return f"{self.tour.title} - Excludes: {self.item}"


class TourNote(models.Model):
    """
    Important notes, restrictions, or conditions for the tour
    """
    NOTE_TYPE_CHOICES = [
        ('general', _("General Note")),
        ('restriction', _("Restriction")),
        ('accessibility', _("Accessibility Note")),
        ('weather', _("Weather Condition")),
        ('important', _("Important")),
    ]
    
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='notes')
    note_type = models.CharField(max_length=20, choices=NOTE_TYPE_CHOICES, default='general')
    content = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = _("Tour Note")
        verbose_name_plural = _("Tour Notes")
        ordering = ['display_order']
    
    def __str__(self):
        return f"{self.tour.title} - {self.get_note_type_display()}"


class ItemToBring(models.Model):
    """
    Items participants should bring with them
    """
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='items_to_bring')
    item = models.CharField(max_length=200)
    is_required = models.BooleanField(default=False, help_text="Is this item required or recommended?")
    icon = models.CharField(max_length=50, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = _("Item to Bring")
        verbose_name_plural = _("Items to Bring")
        ordering = ['-is_required', 'display_order']
    
    def __str__(self):
        required_text = "Required" if self.is_required else "Recommended"
        return f"{self.tour.title} - {required_text}: {self.item}"


class ItineraryItem(models.Model):
    """
    Detailed step-by-step itinerary for the tour
    """
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='itinerary_items')
    step_number = models.PositiveIntegerField(default=1)
    time = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Time or duration for this step (e.g., '09:00 AM' or '2 hours')"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    
    class Meta:
        verbose_name = _("Itinerary Item")
        verbose_name_plural = _("Itinerary Items")
        ordering = ['step_number']
    
    def __str__(self):
        return f"{self.tour.title} - Step {self.step_number}: {self.title}"


class TourAvailability(models.Model):
    """
    Specific dates when a tour is available
    Prepared for integration with bookings app for availability checking
    """
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True, help_text="Optional start time")
    slots_available = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Maximum bookings for this date (leave blank for unlimited)"
    )
    is_available = models.BooleanField(default=True)
    notes = models.CharField(max_length=200, blank=True, help_text="Special notes for this date")
    
    # Future integration point with bookings app
    # The bookings app will query this model to check availability
    # and update slots_available when bookings are made
    
    class Meta:
        verbose_name = _("Tour Availability")
        verbose_name_plural = _("Tour Availabilities")
        ordering = ['date', 'start_time']
        unique_together = [['tour', 'date', 'start_time']]
        indexes = [
            models.Index(fields=['tour', 'date', 'is_available']),
        ]
    
    def __str__(self):
        time_str = f" at {self.start_time}" if self.start_time else ""
        return f"{self.tour.title} - {self.date}{time_str}"


class CancellationPolicyRule(models.Model):
    """
    Flexible cancellation policy rules for tours
    """
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='cancellation_rules')
    hours_before = models.PositiveIntegerField(
        help_text="Hours before tour start (e.g., 24 for '24 hours before')"
    )
    refund_percentage = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)],
        help_text="Percentage of refund (0-100)"
    )
    description = models.CharField(
        max_length=300,
        blank=True,
        help_text="Optional custom description of this rule"
    )
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = _("Cancellation Policy Rule")
        verbose_name_plural = _("Cancellation Policy Rules")
        ordering = ['-hours_before', 'display_order']
    
    def get_description(self):
        """Returns formatted description"""
        if self.description:
            return self.description
        
        if self.hours_before == 0:
            time_text = "Less than 24 hours before"
        elif self.hours_before < 24:
            time_text = f"{self.hours_before} hours before"
        else:
            days = self.hours_before // 24
            time_text = f"{days} day{'s' if days > 1 else ''} before"
        
        if self.refund_percentage == 100:
            return f"Full refund if cancelled {time_text}"
        elif self.refund_percentage == 0:
            return f"No refund if cancelled {time_text}"
        else:
            return f"{self.refund_percentage}% refund if cancelled {time_text}"
    
    def __str__(self):
        return f"{self.tour.title} - {self.get_description()}"


class PickupLocation(models.Model):
    """
    Optional pickup locations for tours
    """
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='pickup_locations')
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, blank=True)
    instructions = models.TextField(blank=True, help_text="Special instructions for this pickup point")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_primary = models.BooleanField(default=False, help_text="Primary/main pickup location")
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = _("Pickup Location")
        verbose_name_plural = _("Pickup Locations")
        ordering = ['-is_primary', 'display_order']
    
    def __str__(self):
        return f"{self.tour.title} - Pickup: {self.name}"
