from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class AboutSection(models.Model):
    """
    Model for the 'Who Are We' section on the homepage and about page.
    Only one active section should exist at a time.
    """
    # Section Information
    section_label = models.CharField(
        max_length=100,
        default="Who Are We",
        help_text="Small label above the heading"
    )
    heading = models.CharField(
        max_length=200,
        default="We Make Dreams Come True",
        help_text="Main heading for the section"
    )
    description = models.TextField(
        help_text="Description text about the company"
    )
    image = models.ImageField(
        upload_to='about/',
        help_text="Image for the about section"
    )
    
    # Statistics
    stat1_number = models.CharField(
        max_length=20,
        default="150+",
        help_text="First statistic number (e.g., 150+)"
    )
    stat1_label = models.CharField(
        max_length=100,
        default="Destinations",
        help_text="Label for first statistic"
    )
    
    stat2_number = models.CharField(
        max_length=20,
        default="20K+",
        help_text="Second statistic number (e.g., 20K+)"
    )
    stat2_label = models.CharField(
        max_length=100,
        default="Happy Clients",
        help_text="Label for second statistic"
    )
    
    stat3_number = models.CharField(
        max_length=20,
        default="98%",
        help_text="Third statistic number (e.g., 98%)"
    )
    stat3_label = models.CharField(
        max_length=100,
        default="Satisfaction",
        help_text="Label for third statistic"
    )
    
    # Management
    is_active = models.BooleanField(
        default=True,
        help_text="Only one section should be active at a time"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Sections"
        ordering = ['-is_active', '-updated_at']
    
    def __str__(self):
        return f"{self.heading} ({'Active' if self.is_active else 'Inactive'})"
    
    def save(self, *args, **kwargs):
        """Ensure only one active section exists"""
        if self.is_active:
            AboutSection.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
