"""
Translation configuration for tours app models.
This file registers which model fields should be translatable using django-modeltranslation.
"""

from modeltranslation.translator import translator, TranslationOptions
from .models import (
    Tour, TourCategory, Language, AccessibilityOption,
    IncludedItem, ExcludedItem, TourNote, ItemToBring,
    ItineraryItem, PickupLocation, CancellationPolicyRule
)


class TourTranslationOptions(TranslationOptions):
    """
    Translatable fields for Tour model.
    When saved, this creates title_en, title_tr, title_ru fields in the database.
    """
    fields = (
        'title',
        'subtitle',
        'short_description',
        'description',
        'duration_text',
        'pickup_information',
        'itinerary_description',
        'meta_description',
    )
    required_languages = ('en',)  # English is required


class TourCategoryTranslationOptions(TranslationOptions):
    """Translatable fields for TourCategory"""
    fields = ('name', 'description')
    required_languages = ('en',)


class LanguageTranslationOptions(TranslationOptions):
    """Translatable fields for Language"""
    fields = ('name',)
    required_languages = ('en',)


class AccessibilityOptionTranslationOptions(TranslationOptions):
    """Translatable fields for AccessibilityOption"""
    fields = ('name', 'description')
    required_languages = ('en',)


class IncludedItemTranslationOptions(TranslationOptions):
    """Translatable fields for IncludedItem"""
    fields = ('item',)
    required_languages = ('en',)


class ExcludedItemTranslationOptions(TranslationOptions):
    """Translatable fields for ExcludedItem"""
    fields = ('item',)
    required_languages = ('en',)


class TourNoteTranslationOptions(TranslationOptions):
    """Translatable fields for TourNote"""
    fields = ('content',)
    required_languages = ('en',)


class ItemToBringTranslationOptions(TranslationOptions):
    """Translatable fields for ItemToBring"""
    fields = ('item',)
    required_languages = ('en',)


class ItineraryItemTranslationOptions(TranslationOptions):
    """Translatable fields for ItineraryItem"""
    fields = ('title', 'description', 'location')
    required_languages = ('en',)


class PickupLocationTranslationOptions(TranslationOptions):
    """Translatable fields for PickupLocation"""
    fields = ('name', 'address', 'instructions')
    required_languages = ('en',)


class CancellationPolicyRuleTranslationOptions(TranslationOptions):
    """Translatable fields for CancellationPolicyRule"""
    fields = ('description',)
    required_languages = ('en',)


# Register all models with their translation options
translator.register(Tour, TourTranslationOptions)
translator.register(TourCategory, TourCategoryTranslationOptions)
translator.register(Language, LanguageTranslationOptions)
translator.register(AccessibilityOption, AccessibilityOptionTranslationOptions)
translator.register(IncludedItem, IncludedItemTranslationOptions)
translator.register(ExcludedItem, ExcludedItemTranslationOptions)
translator.register(TourNote, TourNoteTranslationOptions)
translator.register(ItemToBring, ItemToBringTranslationOptions)
translator.register(ItineraryItem, ItineraryItemTranslationOptions)
translator.register(PickupLocation, PickupLocationTranslationOptions)
translator.register(CancellationPolicyRule, CancellationPolicyRuleTranslationOptions)
