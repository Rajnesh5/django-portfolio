"""
Forms for the Portfolio application.
Handles contact form validation (server-side).
"""
from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """
    Contact form rendered on the contact page.
    Maps directly to the ContactMessage model.
    """
    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Full Name',
            'id': 'contact-name',
            'autocomplete': 'name',
        }),
        error_messages={'required': 'Please enter your name.'}
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email Address',
            'id': 'contact-email',
            'autocomplete': 'email',
        }),
        error_messages={
            'required': 'Please enter your email address.',
            'invalid': 'Please enter a valid email address.',
        }
    )
    subject = forms.CharField(
        max_length=300,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject (optional)',
            'id': 'contact-subject',
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your message...',
            'rows': 5,
            'id': 'contact-message',
        }),
        error_messages={'required': 'Please enter a message.'}
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

    def clean_message(self):
        """Ensure message is at least 10 characters."""
        message = self.cleaned_data.get('message', '')
        if len(message.strip()) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        return message
