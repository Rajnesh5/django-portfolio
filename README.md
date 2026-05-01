# Rajnesh Kr. Ranjan — Personal Portfolio

A modern, production-ready Django portfolio website with glassmorphism design, dark/light mode, animated skill bars, dynamic project cards, and a fully working Gmail contact form.

## Live Preview

Run locally at `http://127.0.0.1:8000/`

---

## Quick Start

### 1. Clone / Open the project
```bash
cd django-portfolio
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
# Copy the example file
copy .env.example .env
```
Then open `.env` and fill in your values (see Gmail SMTP section below).

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Seed sample projects
```bash
python manage.py seed_projects
```

### 6. Create admin superuser
```bash
python manage.py createsuperuser
```

### 7. Start the server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` — your portfolio is live!

---

## Add Your Resume PDF

Place your resume PDF at:
```
core/static/images/resume.pdf
```
The "Download My Resume" button is already wired to this path.

---

## Gmail SMTP Setup Guide

The contact form sends email to your Gmail via SMTP. You **cannot** use your regular Gmail password — you need a Google **App Password**.

### Step-by-step:

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Navigate to **Security** → enable **2-Step Verification** (required)
3. Go to **Security** → **App passwords**
4. Select App: `Mail`, Device: `Other (Custom name)` → type `Portfolio`
5. Click **Generate** — copy the 16-character password shown
6. Open your `.env` file and set:
   ```
   EMAIL_HOST_USER=rajneshranjan5@gmail.com
   EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx   ← paste your app password
   ```

---

## Admin Panel

Access the Django admin at `http://127.0.0.1:8000/admin/`

- **Username:** admin  
- **Password:** Admin@1234  ← Change this immediately in production!

### What you can manage:
- **Projects** — Add, edit, reorder, mark as Featured
- **Contact Messages** — View all form submissions, mark as read

---

## Project Structure

```
django-portfolio/
├── .env                    # Your secret config (not committed to git)
├── .env.example            # Template — safe to commit
├── requirements.txt
├── manage.py
├── portfolio/              # Django project config
│   ├── settings.py
│   └── urls.py
└── core/                   # Main portfolio app
    ├── models.py            # Project + ContactMessage models
    ├── views.py             # Page views + email sending
    ├── forms.py             # ContactForm with validation
    ├── admin.py             # Rich admin panel
    ├── urls.py              # App URL routes
    ├── management/
    │   └── commands/
    │       └── seed_projects.py  # Sample data loader
    ├── static/
    │   ├── css/style.css    # Dark/light mode, glassmorphism
    │   ├── js/main.js       # Typewriter, skill bars, AJAX form
    │   └── images/
    │       └── resume.pdf   # ← PUT YOUR RESUME HERE
    └── templates/
        ├── base.html        # Master layout
        ├── home.html        # Hero + About + Skills + Resume
        ├── projects.html    # Project cards grid
        └── contact.html     # Contact form
```

---

## Features

| Feature | Details |
|---|---|
| **Dark / Light Mode** | Toggle persists via localStorage |
| **Typewriter Effect** | Cycles through your roles |
| **Animated Skill Bars** | Triggered on scroll via IntersectionObserver |
| **Counter Animation** | Years, APIs, productivity stats |
| **AJAX Contact Form** | No page reload, toast notifications |
| **Gmail SMTP** | Contact submissions emailed to you |
| **Django Admin** | Full project + message management |
| **SEO Meta Tags** | Title, description, Open Graph |
| **CSRF Protection** | On all POST forms |
| **Responsive** | Mobile-first, works on all screen sizes |
| **Glassmorphism** | Frosted glass cards throughout |
| **AOS Animations** | Scroll-triggered reveal animations |

---

## Deployment Notes (Production)

1. Set `DEBUG=False` in `.env`
2. Set `ALLOWED_HOSTS=yourdomain.com` in `settings.py`
3. Run `python manage.py collectstatic`
4. Use **Gunicorn** + **Nginx** for serving
5. Use **PostgreSQL** instead of SQLite for the database
6. Generate a strong `SECRET_KEY` and store it securely
