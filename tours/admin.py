from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline, TranslationStackedInline
from .models import (
    Tour, TourImage, TourCategory, Language, AccessibilityOption,
    IncludedItem, ExcludedItem, TourNote, ItemToBring, ItineraryItem,
    TourAvailability, CancellationPolicyRule, PickupLocation
)


# Inline Admin Classes with Translation Support
class IncludedItemInline(TranslationTabularInline):
    model = IncludedItem
    extra = 2
    fields = ('item', 'icon', 'display_order')


class ExcludedItemInline(TranslationTabularInline):
    model = ExcludedItem
    extra = 2
    fields = ('item', 'icon', 'display_order')


class TourNoteInline(TranslationStackedInline):
    model = TourNote
    extra = 1
    fields = ('note_type', 'content', 'icon', 'display_order')
    classes = ['collapse']


class ItemToBringInline(TranslationTabularInline):
    model = ItemToBring
    extra = 2
    fields = ('item', 'is_required', 'icon', 'display_order')


class ItineraryItemInline(TranslationStackedInline):
    model = ItineraryItem
    extra = 1
    fields = ('step_number', 'time', 'title', 'description', 'location')
    classes = ['collapse']


class PickupLocationInline(TranslationStackedInline):
    model = PickupLocation
    extra = 1
    fields = ('name', 'address', 'instructions', 'is_primary', 'display_order', ('latitude', 'longitude'))
    classes = ['collapse']


class CancellationPolicyRuleInline(TranslationTabularInline):
    model = CancellationPolicyRule
    extra = 1
    fields = ('hours_before', 'refund_percentage', 'description', 'display_order')


# Non-translatable inlines
class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1
    fields = ('image', 'caption', 'alt_text', 'is_main', 'display_order')
    classes = ['collapse']


class TourAvailabilityInline(admin.TabularInline):
    model = TourAvailability
    extra = 3
    fields = ('date', 'start_time', 'slots_available', 'is_available', 'notes')
    classes = ['collapse']


# Main Model Admin Classes with Translation Support
@admin.register(Tour)
class TourAdmin(TranslationAdmin):
    list_display = (
        'title', 'difficulty', 'experience_type', 'duration_display',
        'is_active', 'is_featured', 'review_display', 'created_at'
    )
    list_filter = (
        'is_active', 'is_featured', 'difficulty', 'experience_type',
        'categories', 'created_at'
    )
    search_fields = ('title', 'slug', 'short_description', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('review_count', 'rating_average', 'created_at', 'updated_at')
    
    filter_horizontal = ('categories', 'languages', 'accessibility_options')
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title', 'slug', 'subtitle', 'short_description', 'description'
            )
        }),
        ('Tour Characteristics', {
            'fields': (
                ('duration_hours', 'duration_minutes', 'duration_text'),
                'difficulty', 'experience_type',
                'categories', 'languages', 'accessibility_options'
            )
        }),
        ('Content Sections', {
            'fields': ('pickup_information', 'itinerary_description'),
            'classes': ('collapse',)
        }),
        ('Booking Configuration', {
            'fields': (
                ('min_participants', 'max_participants'),
                'booking_cutoff_hours', 'instant_confirmation'
            ),
            'description': 'These settings prepare the tour for integration with the bookings app.'
        }),
        ('Reviews & Ratings', {
            'fields': ('review_count', 'rating_average'),
            'classes': ('collapse',),
            'description': 'Managed automatically by review system'
        }),
        ('Status & Publishing', {
            'fields': ('is_active', 'is_featured', 'published_date')
        }),
        ('SEO & Metadata', {
            'fields': ('meta_description', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [
        TourImageInline,
        ItineraryItemInline,
        IncludedItemInline,
        ExcludedItemInline,
        TourNoteInline,
        ItemToBringInline,
        PickupLocationInline,
        TourAvailabilityInline,
        CancellationPolicyRuleInline,
    ]
    
    def duration_display(self, obj):
        return obj.get_duration_display()
    duration_display.short_description = 'Duration'
    
    def review_display(self, obj):
        if obj.review_count > 0:
            return format_html(
                '<span style="color: #f59e0b;">⭐ {:.1f}</span> ({} reviews)',
                obj.rating_average, obj.review_count
            )
        return format_html('<span style="color: #9ca3af;">{}</span>', 'No reviews')
    review_display.short_description = 'Reviews'
    
    class Media:
        css = {
            'all': ('admin/css/tours_admin.css',)  # Optional: add custom admin styles
        }


@admin.register(TourCategory)
class TourCategoryAdmin(TranslationAdmin):
    list_display = ('name', 'slug', 'icon', 'display_order', 'tour_count')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('display_order', 'name')
    
    def tour_count(self, obj):
        count = obj.tours.count()
        return format_html('<strong>{}</strong> tour{}', count, 's' if count != 1 else '')
    tour_count.short_description = 'Tours'


@admin.register(Language)
class LanguageAdmin(TranslationAdmin):
    list_display = ('name', 'code', 'tour_count')
    search_fields = ('name', 'code')
    ordering = ('name',)
    
    def tour_count(self, obj):
        return obj.tours.count()
    tour_count.short_description = 'Tours Using This Language'


@admin.register(AccessibilityOption)
class AccessibilityOptionAdmin(TranslationAdmin):
    list_display = ('name', 'icon', 'tour_count')
    search_fields = ('name', 'description')
    ordering = ('name',)
    
    def tour_count(self, obj):
        return obj.tours.count()
    tour_count.short_description = 'Tours'


@admin.register(TourImage)
class TourImageAdmin(admin.ModelAdmin):
    list_display = ('tour', 'caption', 'is_main', 'display_order', 'image_preview')
    list_filter = ('is_main', 'tour')
    search_fields = ('tour__title', 'caption', 'alt_text')
    ordering = ('tour', '-is_main', 'display_order')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px; object-fit: cover;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = 'Preview'


@admin.register(TourAvailability)
class TourAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('tour', 'date', 'start_time', 'slots_available', 'is_available', 'notes')
    list_filter = ('is_available', 'date', 'tour')
    search_fields = ('tour__title', 'notes')
    date_hierarchy = 'date'
    ordering = ('-date', 'start_time')
    
    # Future integration point: The bookings app will interact with this model
    # to check and update availability


# Register remaining models with Translation admin support
@admin.register(IncludedItem)
class IncludedItemAdmin(TranslationAdmin):
    list_display = ('tour', 'item', 'icon', 'display_order')
    list_filter = ('tour',)
    search_fields = ('tour__title', 'item')


@admin.register(ExcludedItem)
class ExcludedItemAdmin(TranslationAdmin):
    list_display = ('tour', 'item', 'icon', 'display_order')
    list_filter = ('tour',)
    search_fields = ('tour__title', 'item')


@admin.register(TourNote)
class TourNoteAdmin(TranslationAdmin):
    list_display = ('tour', 'note_type', 'content_preview', 'display_order')
    list_filter = ('note_type', 'tour')
    search_fields = ('tour__title', 'content')
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'


@admin.register(ItemToBring)
class ItemToBringAdmin(TranslationAdmin):
    list_display = ('tour', 'item', 'is_required', 'icon', 'display_order')
    list_filter = ('is_required', 'tour')
    search_fields = ('tour__title', 'item')


@admin.register(ItineraryItem)
class ItineraryItemAdmin(admin.ModelAdmin):
    list_display = ('tour', 'step_number', 'title', 'time', 'location')
    list_filter = ('tour',)
    search_fields = ('tour__title', 'title', 'description', 'location')
    ordering = ('tour', 'step_number')


@admin.register(CancellationPolicyRule)
class CancellationPolicyRuleAdmin(admin.ModelAdmin):
    list_display = ('tour', 'hours_before', 'refund_percentage', 'policy_description')
    list_filter = ('refund_percentage', 'tour')
    search_fields = ('tour__title', 'description')
    
    def policy_description(self, obj):
        return obj.get_description()
    policy_description.short_description = 'Policy'


@admin.register(PickupLocation)
class PickupLocationAdmin(admin.ModelAdmin):
    list_display = ('tour', 'name', 'is_primary', 'address', 'display_order')
    list_filter = ('is_primary', 'tour')
    search_fields = ('tour__title', 'name', 'address')
