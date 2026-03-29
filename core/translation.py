"""
Translation configuration for core app models.
This file registers which model fields should be translatable using django-modeltranslation.
"""

from modeltranslation.translator import translator, TranslationOptions
from .models import AboutSection


class AboutSectionTranslationOptions(TranslationOptions):
    """
    Translatable fields for AboutSection model.
    When saved, this creates field_en, field_tr, field_ru versions in the database.
    """
    fields = (
        'section_label',
        'heading',
        'description',
        'stat1_label',
        'stat2_label',
        'stat3_label',
    )
    required_languages = ('en',)  # English is required


# Register the model with its translation options
translator.register(AboutSection, AboutSectionTranslationOptions)
