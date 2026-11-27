/* ==========================================================================
   MADSON DIGITAL — Comportamento
   Sem dependências externas. Funciona em qualquer hospedagem estática.
   ========================================================================== */
(function () {
  'use strict';

  var cfg = window.MADSON_CONFIG || {};
  var root = document.documentElement;
  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  /* ---- Canais de contato ------------------------------------------------ */
  function digits(value) { return String(value || '').replace(/\D/g, ''); }

  function whatsappUrl(text) {
    var number = digits(cfg.whatsapp);
    if (!number) return null;
    return 'https://wa.me/' + number + '?text=' + encodeURIComponent(text || cfg.whatsappGreeting || '');
  }

  function emailUrl(subject, body) {
    if (!cfg.email) return null;
    return 'mailto:' + cfg.email + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  }

  function formatPhone(value) {
    var n = digits(value);
    if (n.length === 13 && n.indexOf('55') === 0) {
      var ddd = n.slice(2, 4), rest = n.slice(4);
      return '+55 ' + ddd + ' ' + rest.slice(0, 5) + '-' + rest.slice(5);
    }
    return n ? '+' + n : '';
  }

  function applyContacts() {
    var wa = whatsappUrl(cfg.whatsappGreeting);
    var mail = emailUrl('Contato pelo site', '');

    $$('[data-whatsapp]').forEach(function (el) {
      if (!wa) { el.hidden = true; return; }
      el.setAttribute('href', wa);
      if (el.tagName === 'A') {
        el.setAttribute('target', '_blank');
        el.setAttribute('rel', 'noopener noreferrer');
      }
    });

    $$('[data-email]').forEach(function (el) {
      if (!mail) { el.hidden = true; return; }
      el.setAttribute('href', mail);
    });

    $$('[data-phone-text]').forEach(function (el) { el.textContent = formatPhone(cfg.whatsapp); });
    $$('[data-email-text]').forEach(function (el) { el.textContent = cfg.email || ''; });
    $$('[data-year]').forEach(function (el) { el.textContent = String(new Date().getFullYear()); });

    if (!wa) $$('[data-requires="whatsapp"]').forEach(function (el) { el.hidden = true; });
    if (!cfg.email) $$('[data-requires="email"]').forEach(function (el) { el.hidden = true; });

    // Redes sociais: só aparecem se perfis reais forem cadastrados em config.js.
    var socialCol = $('[data-social-col]');
    if (socialCol) {
      var socials = Array.isArray(cfg.socials) ? cfg.socials : [];
      if (!socials.length) { socialCol.hidden = true; return; }
      var list = $('[data-socials]', socialCol);
      socials.forEach(function (item) {
        if (!item || !item.name || !item.url) return;
        var li = document.createElement('li');
        var a = document.createElement('a');
        a.href = item.url;
        a.target = '_blank';
        a.rel = 'noopener noreferrer';
        a.textContent = item.name + ' ↗';
        li.appendChild(a);
        list.appendChild(li);
      });
      socialCol.hidden = false;
    }
  }

  /* ---- Cabeçalho e navegação mobile ------------------------------------- */
  function initHeader() {
    var header = $('.site-header');
    if (header) {
      var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 12); };
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    }

    var toggle = $('.nav-toggle');
    var nav = $('#primary-nav');
    if (!toggle || !nav) return;

    var setOpen = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('is-open', open);
      if (header) header.classList.toggle('is-open', open);
      toggle.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    };

    setOpen(false);
    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    $$('.nav__link', nav).forEach(function (link) {
      link.addEventListener('click', function () { setOpen(false); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        toggle.focus();
      }
    });
    document.addEventListener('click', function (e) {
      if (toggle.getAttribute('aria-expanded') === 'true' &&
          !nav.contains(e.target) && !toggle.contains(e.target)) setOpen(false);
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 900 && toggle.getAttribute('aria-expanded') === 'true') setOpen(false);
    });
  }

  /* ---- Animações discretas + link ativo --------------------------------- */
  function initReveal() {
    var items = $$('.reveal');
    if (!items.length) return;
    if (!('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-visible'); });
      return;
    }
    root.classList.add('anim-ready');
    var observer = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    items.forEach(function (el) { observer.observe(el); });
  }

  function initActiveNav() {
    var links = $$('.nav__link[href^="#"]');
    if (!links.length || !('IntersectionObserver' in window)) return;
    var sections = links.map(function (a) { return $(a.getAttribute('href')); }).filter(Boolean);
    if (!sections.length) return;
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (a) {
          if (a.getAttribute('href') === '#' + entry.target.id) a.setAttribute('aria-current', 'page');
          else a.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-35% 0px -55% 0px' });
    sections.forEach(function (s) { observer.observe(s); });
  }

  /* ---- Abas dos planos (acessíveis por teclado) ------------------------- */
  function initTabs() {
    var tablist = $('[role="tablist"]');
    if (!tablist) return;
    var tabs = $$('[role="tab"]', tablist);

    function select(tab, moveFocus) {
      tabs.forEach(function (t) {
        var active = t === tab;
        t.setAttribute('aria-selected', String(active));
        t.setAttribute('tabindex', active ? '0' : '-1');
        var panel = document.getElementById(t.getAttribute('aria-controls'));
        if (panel) panel.hidden = !active;
      });
      if (moveFocus) tab.focus();
    }

    tabs.forEach(function (tab, index) {
      tab.addEventListener('click', function () { select(tab, false); });
      tab.addEventListener('keydown', function (e) {
        var next = null;
        if (e.key === 'ArrowRight') next = tabs[(index + 1) % tabs.length];
        else if (e.key === 'ArrowLeft') next = tabs[(index - 1 + tabs.length) % tabs.length];
        else if (e.key === 'Home') next = tabs[0];
        else if (e.key === 'End') next = tabs[tabs.length - 1];
        if (next) { e.preventDefault(); select(next, true); }
      });
    });
    select(tabs.find(function (t) { return t.getAttribute('aria-selected') === 'true'; }) || tabs[0], false);
  }

  /* ---- Pré-seleção de plano/serviço no formulário ----------------------- */
  function initPrefill() {
    var select = $('#tipo');
    var status = $('#form-status');
    if (!select) return;
    $$('[data-prefill]').forEach(function (el) {
      el.addEventListener('click', function () {
        var value = el.getAttribute('data-prefill');
        var exists = Array.prototype.some.call(select.options, function (o) { return o.value === value; });
        if (!exists) return;
        select.value = value;
        select.removeAttribute('aria-invalid');
        var err = $('[data-error-for="tipo"]');
        if (err) err.textContent = '';
        if (status) status.textContent = 'Selecionamos "' + value + '" para você. Complete os campos e envie.';
      });
    });
  }

  /* ---- Formulário: validação + entrega real ----------------------------- */
  function initForm() {
    var form = $('#contact-form');
    if (!form) return;
    var status = $('#form-status');

    var validators = {
      nome: function (v) { return v.trim().length >= 2 || 'Informe seu nome completo.'; },
      telefone: function (v) {
        var n = digits(v);
        return (n.length >= 10 && n.length <= 13) || 'Informe um telefone válido com DDD.';
      },
      email: function (v) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) || 'Informe um e-mail válido.';
      },
      tipo: function (v) { return !!v || 'Selecione o tipo de projeto.'; },
      descricao: function (v) { return v.trim().length >= 20 || 'Descreva o projeto com pelo menos 20 caracteres.'; },
      consent: function (v, el) { return el.checked || 'Autorize o contato para continuar.'; }
    };

    function setError(name, message) {
      var el = form.elements[name];
      var box = $('[data-error-for="' + name + '"]', form);
      if (box) box.textContent = message || '';
      if (el) {
        if (message) el.setAttribute('aria-invalid', 'true');
        else el.removeAttribute('aria-invalid');
      }
    }

    function validate() {
      var valid = true, firstInvalid = null;
      Object.keys(validators).forEach(function (name) {
        var el = form.elements[name];
        if (!el) return;
        var result = validators[name](el.value || '', el);
        if (result === true) { setError(name, ''); return; }
        setError(name, result);
        valid = false;
        if (!firstInvalid) firstInvalid = el;
      });
      if (firstInvalid) {
        firstInvalid.focus();
        if (status) status.textContent = 'Revise os campos destacados antes de enviar.';
      }
      return valid;
    }

    Object.keys(validators).forEach(function (name) {
      var el = form.elements[name];
      if (!el) return;
      var clear = function () { setError(name, ''); };
      el.addEventListener('input', clear);
      el.addEventListener('change', clear);
    });

    function buildMessage(data) {
      return [
        'Novo contato — site Madson Digital',
        '',
        'Nome: ' + (data.nome || '').trim(),
        'Empresa: ' + ((data.empresa || '').trim() || 'Não informada'),
        'Telefone: ' + (data.telefone || '').trim(),
        'E-mail: ' + (data.email || '').trim(),
        'Tipo de projeto: ' + (data.tipo || '').trim(),
        '',
        'Descrição:',
        (data.descricao || '').trim()
      ].join('\n');
    }

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!validate()) return;

      var data = {};
      Array.from(new FormData(form).entries()).forEach(function (pair) { data[pair[0]] = pair[1]; });
      var text = buildMessage(data);
      var action = (event.submitter && event.submitter.value) || 'whatsapp';

      if (action === 'email') {
        var mail = emailUrl('Novo contato — site Madson Digital', text);
        if (!mail) {
          if (status) status.textContent = 'O e-mail de destino não está configurado.';
          return;
        }
        window.location.href = mail;
        if (status) status.textContent = 'Seu aplicativo de e-mail foi aberto com a mensagem pronta. Confirme o envio por lá.';
        return;
      }

      var wa = whatsappUrl(text);
      if (!wa) {
        if (status) status.textContent = 'O WhatsApp não está configurado. Use o envio por e-mail.';
        return;
      }
      // Abrimos um link real: nenhum dado é enviado ou armazenado por este site.
      var link = document.createElement('a');
      link.href = wa;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.style.display = 'none';
      document.body.appendChild(link);
      link.click();
      link.remove();
      if (status) status.textContent = 'Abrimos o WhatsApp com a mensagem pronta. Conclua o envio no aplicativo.';
    });
  }

  /* ---- Inicialização ---------------------------------------------------- */
  function init() {
    applyContacts();
    initHeader();
    initReveal();
    initActiveNav();
    initTabs();
    initPrefill();
    initForm();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
