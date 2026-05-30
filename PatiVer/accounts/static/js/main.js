document.addEventListener('DOMContentLoaded', function() {
  // Navbar scroll
  const navbar = document.querySelector('.navbar');
  window.addEventListener('scroll', () => {
    navbar && navbar.classList.toggle('scrolled', window.scrollY > 10);
  });

  // Auto-hide messages
  document.querySelectorAll('.msg').forEach(el => {
    setTimeout(() => el.remove(), 5000);
  });

  // Mobile nav toggle
  const toggle = document.querySelector('.nav-toggle');
  const center = document.querySelector('.nav-center');
  if (toggle && center) {
    toggle.addEventListener('click', () => center.classList.toggle('open'));
    document.addEventListener('click', e => {
      if (!toggle.contains(e.target) && !center.contains(e.target))
        center.classList.remove('open');
    });
  }
});
