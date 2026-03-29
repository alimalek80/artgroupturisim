from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import AboutSection


@admin.register(AboutSection)
class AboutSectionAdmin(TranslationAdmin):
    list_display = ['heading', 'section_label', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['heading', 'description', 'section_label']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Section Content', {
            'fields': ('section_label', 'heading', 'description', 'image')
        }),
        ('Statistics', {
            'fields': (
                ('stat1_number', 'stat1_label'),
                ('stat2_number', 'stat2_label'),
                ('stat3_number', 'stat3_label'),
            )
        }),
        ('Management', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Show warning message if multiple sections exist"""
        super().save_model(request, obj, form, change)
        if obj.is_active:
            self.message_user(
                request,
                f"'{obj.heading}' is now the active About section. Other sections have been deactivated."
            )
