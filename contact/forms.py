from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """
    Contact form for the home page
    """
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Name',
                'class': 'w-full px-6 py-5 rounded-2xl bg-slate-50 border-2 border-transparent focus:border-orange-500 focus:bg-white transition-all font-bold'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address',
                'class': 'w-full px-6 py-5 rounded-2xl bg-slate-50 border-2 border-transparent focus:border-orange-500 focus:bg-white transition-all font-bold'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Phone Number',
                'class': 'w-full px-6 py-5 rounded-2xl bg-slate-50 border-2 border-transparent focus:border-orange-500 focus:bg-white transition-all font-bold'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Tell us about your dream trip...',
                'rows': 6,
                'class': 'w-full px-6 py-5 rounded-2xl bg-slate-50 border-2 border-transparent focus:border-orange-500 focus:bg-white transition-all font-bold resize-none'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields required except phone
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = False
        self.fields['message'].required = True
