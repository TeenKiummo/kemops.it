(() => {
  'use strict';
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const header = $('.site-header');
  const menu = $('.mobile-menu');
  const menuButton = $('.mobile-toggle');
  const meter = $('.scroll-meter-fill');
  const glow = $('.cursor-glow');
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const coarsePointer = matchMedia('(pointer: coarse)');

  const year = $('#year');
  if (year) year.textContent = String(new Date().getFullYear());

  function closeMenu() {
    menu.hidden = true;
    document.body.classList.remove('menu-open');
    menuButton.classList.remove('open');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Apri menu');
  }
  if (menu && menuButton) {
    menuButton.addEventListener('click', () => {
      if (!menu.hidden) return closeMenu();
      menu.hidden = false;
      document.body.classList.add('menu-open');
      menuButton.classList.add('open');
      menuButton.setAttribute('aria-expanded', 'true');
      menuButton.setAttribute('aria-label', 'Chiudi menu');
      $('a', menu)?.focus();
    });
    $$('a', menu).forEach(a => a.addEventListener('click', closeMenu));
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && !menu.hidden) {
        closeMenu();
        menuButton.focus();
      }
    });
    window.addEventListener('resize', () => {
      if (innerWidth > 1150 && !menu.hidden) closeMenu();
    });
  }

  if ('IntersectionObserver' in window && !reduceMotion.matches) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: .07, rootMargin: '0px 0px -25px 0px' });
    $$('.reveal').forEach(el => observer.observe(el));
  } else {
    $$('.reveal').forEach(el => el.classList.add('visible'));
  }

  let pending = false;
  function updateScroll() {
    const y = scrollY || document.documentElement.scrollTop;
    const available = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    if (meter) meter.style.width = `${Math.min(100, (y / available) * 100)}%`;
    header?.classList.toggle('scrolled', y > 30);
    pending = false;
  }
  addEventListener('scroll', () => {
    if (!pending) {
      pending = true;
      requestAnimationFrame(updateScroll);
    }
  }, { passive: true });
  updateScroll();

  if (glow && !reduceMotion.matches && !coarsePointer.matches) {
    let pendingPointer = false;
    addEventListener('pointermove', event => {
      if (pendingPointer) return;
      pendingPointer = true;
      requestAnimationFrame(() => {
        glow.style.opacity = '1';
        glow.style.left = `${event.clientX}px`;
        glow.style.top = `${event.clientY}px`;
        pendingPointer = false;
      });
    }, { passive: true });
  }
})();
