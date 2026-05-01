"""
Management command to seed the database with sample projects.
Run: python manage.py seed_projects
"""
from django.core.management.base import BaseCommand
from core.models import Project


SAMPLE_PROJECTS = [
    {
        'title': 'AI-Powered API Generator',
        'short_description': 'An intelligent tool that generates production-ready REST APIs from plain English descriptions, reducing development time from days to under 1 hour.',
        'description': 'Built at TCS, this AI-powered API generator uses NLP to parse natural language requirements and auto-generates fully documented Django/FastAPI endpoints with validation, authentication, and tests. Boosted team productivity by 60%+.',
        'tech_stack': 'Python, FastAPI, Django, OpenAI API, PostgreSQL, Docker',
        'github_url': 'https://github.com/',
        'live_url': '',
        'is_featured': True,
        'order': 1,
    },
    {
        'title': 'Scalable REST API Platform',
        'short_description': 'Architected and maintained 100+ scalable REST APIs with a strong focus on reliability, performance, and low defect rates at TCS.',
        'description': 'Led the design and development of a comprehensive REST API platform serving millions of requests. Implemented caching, rate limiting, and advanced monitoring. Achieved 40% reduction in response times through query optimisation.',
        'tech_stack': 'Django REST Framework, PostgreSQL, Redis, AWS EC2, Nginx, CI/CD',
        'github_url': 'https://github.com/',
        'live_url': '',
        'is_featured': True,
        'order': 2,
    },
    {
        'title': 'HIPAA-Compliant Healthcare Data Pipeline',
        'short_description': 'Processed 50K+ patient records daily using optimised SQL queries and stored procedures, ensuring HIPAA-compliant data integrity.',
        'description': 'At Cognizant, developed a robust data processing pipeline handling 50,000+ patient records daily. Improved database performance by 35% through strategic indexing and query optimisation. Automated reporting workflows reducing manual effort by 70%.',
        'tech_stack': 'SQL, PostgreSQL, MySQL, Python, Stored Procedures, Medidata Rave',
        'github_url': 'https://github.com/',
        'live_url': '',
        'is_featured': True,
        'order': 3,
    },
    {
        'title': 'Test Automation Framework',
        'short_description': 'Automated 200+ test cases achieving 100% test coverage, improving testing efficiency by 60%.',
        'description': 'Designed and implemented a comprehensive test automation framework at TCS. Executed TDD practices, streamlined requirements documentation, and eliminated post-deployment bugs through rigorous automated testing pipelines.',
        'tech_stack': 'Python, Pytest, Selenium, CI/CD, Git, Jenkins',
        'github_url': 'https://github.com/',
        'live_url': '',
        'is_featured': False,
        'order': 4,
    },
    {
        'title': 'Microservices Architecture System',
        'short_description': 'Designed and implemented a microservices-based architecture for a high-traffic application, ensuring 99.9% uptime and horizontal scalability.',
        'description': 'Led the migration from a monolithic application to a microservices architecture. Implemented service discovery, API gateways, and event-driven communication using message queues. Deployed on AWS with auto-scaling groups.',
        'tech_stack': 'Python, FastAPI, AWS Lambda, SQS, S3, Docker, PostgreSQL',
        'github_url': 'https://github.com/',
        'live_url': '',
        'is_featured': False,
        'order': 5,
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample portfolio projects'

    def handle(self, *args, **kwargs):
        created = 0
        for data in SAMPLE_PROJECTS:
            obj, is_new = Project.objects.get_or_create(title=data['title'], defaults=data)
            if is_new:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  [OK] Created: {obj.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'  [SKIP] Already exists: {obj.title}'))

        self.stdout.write(self.style.SUCCESS(f'\nDone! {created} new project(s) added.'))
