document.addEventListener('DOMContentLoaded', function () {
  const navToggle = document.querySelector('.nav-toggle');
  const mainNav = document.querySelector('.main-nav');

  if (navToggle && mainNav) {
    navToggle.addEventListener('click', function () {
      const isOpen = mainNav.classList.toggle('is-open');
      this.setAttribute('aria-expanded', String(isOpen));
    });
  }

  document.querySelectorAll('form').forEach((form) => {
    form.addEventListener('submit', function () {
      const submit = this.querySelector('button[type="submit"]');
      if (submit) {
        submit.disabled = true;
        submit.dataset.originalText = submit.textContent;
        submit.textContent = 'Submitting…';
        this.classList.add('is-loading');
      }
    });
  });

  document.querySelectorAll('[data-table-target]').forEach((input) => {
    const targetId = input.dataset.tableTarget;
    const table = document.querySelector(targetId);
    if (!table) return;

    input.addEventListener('input', function () {
      const filter = this.value.toLowerCase().trim();
      const rows = table.querySelectorAll('tbody tr');

      rows.forEach((row) => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(filter) ? '' : 'none';
      });
    });
  });
});
