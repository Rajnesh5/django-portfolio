/* =====================================================
   Portfolio JavaScript
   Dark/Light Mode | Typewriter | Skill Bars | AJAX Form
   ===================================================== */

document.addEventListener('DOMContentLoaded', () => {

  // ── 1. Dark / Light Mode Toggle ──────────────────────
  const themeToggle = document.getElementById('themeToggle');
  const savedTheme  = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next    = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
      updateThemeIcon(next);
    });
  }

  function updateThemeIcon(theme) {
    if (!themeToggle) return;
    themeToggle.innerHTML = theme === 'dark'
      ? '<i class="fas fa-sun"></i>'
      : '<i class="fas fa-moon"></i>';
    themeToggle.title = theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
  }

  // ── 2. AOS (Animate on Scroll) init ──────────────────
  if (typeof AOS !== 'undefined') {
    AOS.init({ duration: 700, easing: 'ease-out-cubic', once: true, offset: 60 });
  }

  // ── 3. Typewriter Effect ──────────────────────────────
  const typeEl = document.getElementById('typewriter-text');
  if (typeEl) {
    const roles = [
      'Lead Backend Engineer',
      'Python & Django Expert',
      'REST API Architect',
      'AWS Cloud Practitioner',
      'AI Automation Builder',
    ];
    let roleIdx = 0, charIdx = 0, deleting = false;

    function typeWrite() {
      const current = roles[roleIdx];
      if (deleting) {
        typeEl.textContent = current.substring(0, charIdx--);
      } else {
        typeEl.textContent = current.substring(0, charIdx++);
      }

      let delay = deleting ? 50 : 100;
      if (!deleting && charIdx > current.length) {
        delay = 2000; deleting = true;
      } else if (deleting && charIdx < 0) {
        deleting = false; charIdx = 0;
        roleIdx = (roleIdx + 1) % roles.length;
        delay = 400;
      }
      setTimeout(typeWrite, delay);
    }
    typeWrite();
  }

  // ── 4. Skill Bar Animations ───────────────────────────
  const skillBars = document.querySelectorAll('.skill-bar-fill');
  if (skillBars.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const fill = entry.target;
          fill.style.width = fill.dataset.level + '%';
          observer.unobserve(fill);
        }
      });
    }, { threshold: 0.3 });

    skillBars.forEach(bar => observer.observe(bar));
  }

  // ── 5. Navbar active link ─────────────────────────────
  const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
  const sections = document.querySelectorAll('section[id]');

  window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(sec => {
      if (window.scrollY >= sec.offsetTop - 100) current = sec.id;
    });
    navLinks.forEach(link => {
      link.classList.toggle('active', link.getAttribute('href') === `#${current}`);
    });
  }, { passive: true });

  // ── 6. Contact Form AJAX ──────────────────────────────
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn     = contactForm.querySelector('[type="submit"]');
      const spinner = btn.querySelector('.spinner');
      const btnText = btn.querySelector('.btn-text');

      // Client-side validation
      if (!contactForm.checkValidity()) {
        contactForm.reportValidity();
        return;
      }

      btn.disabled = true;
      if (spinner) spinner.classList.remove('d-none');
      if (btnText) btnText.textContent = 'Sending…';

      try {
        const formData = new FormData(contactForm);
        const response = await fetch(contactForm.action, {
          method: 'POST',
          headers: { 'X-Requested-With': 'XMLHttpRequest' },
          body: formData,
        });
        const data = await response.json();

        if (data.status === 'success') {
          showToast(data.message, 'success');
          contactForm.reset();
        } else {
          const errorMsg = data.message || 'Please check the form and try again.';
          showToast(errorMsg, 'error');

          // Show field-level errors
          if (data.errors) {
            Object.entries(data.errors).forEach(([field, msgs]) => {
              const input = document.getElementById(`contact-${field}`);
              if (input) {
                input.classList.add('is-invalid');
                let feedback = input.nextElementSibling;
                if (!feedback || !feedback.classList.contains('invalid-feedback')) {
                  feedback = document.createElement('div');
                  feedback.className = 'invalid-feedback';
                  input.after(feedback);
                }
                feedback.textContent = msgs.join(' ');
              }
            });
          }
        }
      } catch {
        showToast('Something went wrong. Please try again later.', 'error');
      } finally {
        btn.disabled = false;
        if (spinner) spinner.classList.add('d-none');
        if (btnText) btnText.textContent = 'Send Message';
      }
    });

    // Clear invalid state on input
    contactForm.querySelectorAll('.form-control').forEach(input => {
      input.addEventListener('input', () => input.classList.remove('is-invalid'));
    });
  }

  // ── 7. Toast Helper ───────────────────────────────────
  function showToast(message, type = 'success') {
    let container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }

    const icon  = type === 'success' ? '✅' : '❌';
    const color = type === 'success' ? '#10b981' : '#ef4444';

    const toast = document.createElement('div');
    toast.className = `custom-toast ${type}`;
    toast.innerHTML = `
      <span style="font-size:1.3rem">${icon}</span>
      <div>
        <div style="font-weight:600;color:${color}">${type === 'success' ? 'Success!' : 'Error'}</div>
        <div style="font-size:0.88rem;color:var(--text-secondary)">${message}</div>
      </div>
    `;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.animation = 'slideInRight 0.3s ease reverse';
      setTimeout(() => toast.remove(), 300);
    }, 4500);
  }

  // ── 8. Smooth scroll for anchor links ────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ── 9. Counter animation ──────────────────────────────
  const counters = document.querySelectorAll('.counter-num');
  if (counters.length) {
    const counterObs = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el     = entry.target;
          const target = parseInt(el.dataset.target);
          const suffix = el.dataset.suffix || '';
          let current  = 0;
          const step   = Math.ceil(target / 60);
          const timer  = setInterval(() => {
            current = Math.min(current + step, target);
            el.textContent = current + suffix;
            if (current >= target) clearInterval(timer);
          }, 25);
          counterObs.unobserve(el);
        }
      });
    }, { threshold: 0.5 });

    counters.forEach(c => counterObs.observe(c));
  }

}); // end DOMContentLoaded
