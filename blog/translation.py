"""
Translation configuration for blog app models.
This file registers which model fields should be translatable using django-modeltranslation.
"""

from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Post


class CategoryTranslationOptions(TranslationOptions):
    """
    Translatable fields for Category model.
    Creates name_en, name_tr, name_ru, etc. in the database.
    """
    fields = ('name', 'description')
    required_languages = ('en',)  # English is required


class PostTranslationOptions(TranslationOptions):
    """
    Translatable fields for Post model.
    All content and SEO fields are translatable.
    """
    fields = (
        # Content fields
        'title',
        'excerpt',
        'content',
        
        # SEO fields
        'meta_title',
        'meta_description',
        'meta_keywords',
        
        # Open Graph fields
        'og_title',
        'og_description',
    )
    required_languages = ('en',)  # English is required


# Register models with their translation options
translator.register(Category, CategoryTranslationOptions)
translator.register(Post, PostTranslationOptions)
