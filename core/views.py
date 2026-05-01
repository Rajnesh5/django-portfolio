"""
Views for the Portfolio application.
Handles page rendering, contact form processing, and email sending.
"""
import logging
import mimetypes
import os

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.mail import send_mail
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import ContactForm
from .models import Project

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────
# Skills data (defined here so it's easy to update)
# ─────────────────────────────────────────────────────────────
SKILLS = [
    # Backend
    {'name': 'Python',       'level': 95, 'category': 'Backend'},
    {'name': 'Django',       'level': 90, 'category': 'Backend'},
    {'name': 'FastAPI',      'level': 85, 'category': 'Backend'},
    {'name': 'REST APIs',    'level': 92, 'category': 'Backend'},
    {'name': 'Flask',        'level': 80, 'category': 'Backend'},
    # Database
    {'name': 'PostgreSQL',   'level': 85, 'category': 'Database'},
    {'name': 'MySQL',        'level': 82, 'category': 'Database'},
    {'name': 'SQL',          'level': 88, 'category': 'Database'},
    # Cloud & DevOps
    {'name': 'AWS (EC2/S3/Lambda)', 'level': 75, 'category': 'Cloud'},
    {'name': 'CI/CD',        'level': 78, 'category': 'Cloud'},
    {'name': 'Git',          'level': 90, 'category': 'Cloud'},
    # Architecture
    {'name': 'System Design',       'level': 80, 'category': 'Architecture'},
    {'name': 'Microservices',       'level': 78, 'category': 'Architecture'},
    {'name': 'Database Optimization','level': 82, 'category': 'Architecture'},
]


def home(request):
    """
    Home page view — renders the hero, about, skills, and resume sections.
    Featured projects are loaded from the database.
    """
    featured_projects = Project.objects.filter(is_featured=True)[:3]
    context = {
        'skills': SKILLS,
        'featured_projects': featured_projects,
        'extra_skills': [
            'Microservices', 'TDD', 'Agile/Scrum', 'Docker', 'Redis',
            'Celery', 'DRF', 'Swagger', 'Postman', 'Linux', 'Nginx', 'JWT Auth',
        ],
        'page_title': 'Rajnesh Kr. Ranjan | Lead Backend Engineer',
        'page_description': (
            'Lead Backend Engineer with 4+ years of experience building scalable systems, '
            'REST APIs, and AI-powered automation. Expert in Python, Django, FastAPI, and AWS.'
        ),
    }
    return render(request, 'home.html', context)



def download_resume(request):
    """
    Serve the resume PDF with explicit HttpResponse for maximum
    browser compatibility (avoids Chrome UUID filename bug with FileResponse).
    """
    file_path = finders.find('images/resume.pdf')
    if not file_path or not os.path.exists(file_path):
        raise Http404("Resume not found.")

    with open(file_path, 'rb') as f:
        pdf_data = f.read()

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename="Rajnesh_Kr_Ranjan_Resume.pdf"; '
        "filename*=UTF-8''Rajnesh_Kr_Ranjan_Resume.pdf"
    )
    response['Content-Length'] = len(pdf_data)
    return response


def projects(request):
    """
    Projects page — shows all portfolio projects with optional category filtering.
    """
    all_projects = Project.objects.all()
    context = {
        'projects': all_projects,
        'page_title': 'Projects | Rajnesh Kr. Ranjan',
        'page_description': 'Explore my portfolio of backend engineering, API design, and AI-powered projects.',
    }
    return render(request, 'projects.html', context)


@require_http_methods(["GET", "POST"])
def contact(request):
    """
    Contact page — renders the form on GET.
    On POST, validates, saves to DB, and sends email notification.
    Returns JSON for AJAX submissions.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if form.is_valid():
            # Save to database
            contact_msg = form.save()

            # Send email notification
            try:
                send_mail(
                    subject=f"[Portfolio] New message from {contact_msg.name}: {contact_msg.subject or 'No Subject'}",
                    message=(
                        f"You have a new portfolio contact form submission:\n\n"
                        f"Name:    {contact_msg.name}\n"
                        f"Email:   {contact_msg.email}\n"
                        f"Subject: {contact_msg.subject}\n\n"
                        f"Message:\n{contact_msg.message}\n\n"
                        f"---\nSent from your portfolio website."
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                email_sent = True
            except Exception as e:
                logger.error("Failed to send contact email: %s", str(e))
                email_sent = False

            if is_ajax:
                return JsonResponse({
                    'status': 'success',
                    'message': "Thank you! Your message has been received. I'll get back to you shortly.",
                    'email_sent': email_sent,
                })
            # Non-AJAX fallback: redirect with session message
            return render(request, 'contact.html', {
                'form': ContactForm(),
                'success': True,
                'page_title': 'Contact | Rajnesh Kr. Ranjan',
            })
        else:
            # Form invalid
            if is_ajax:
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors,
                    'message': 'Please correct the errors below.',
                }, status=400)

    else:
        form = ContactForm()

    return render(request, 'contact.html', {
        'form': form,
        'page_title': 'Contact | Rajnesh Kr. Ranjan',
        'page_description': 'Get in touch with Rajnesh Kr. Ranjan for collaboration, job opportunities, or project inquiries.',
    })
