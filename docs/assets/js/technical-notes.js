/* Progressive enhancement: the catalog and full-size image links work without JS. */
(() => {
  'use strict';
  // Kramdown emits legacy MathJax script nodes; convert them before MathJax 3 starts.
  document.querySelectorAll('script[type^="math/tex"]').forEach(node => {
    const display = node.type.includes('mode=display');
    const replacement = document.createElement(display ? 'div' : 'span');
    replacement.className = display ? 'equation' : 'inline-equation';
    replacement.textContent = (display ? '\\[' : '\\(') + node.textContent + (display ? '\\]' : '\\)');
    node.replaceWith(replacement);
  });
  const catalog = document.getElementById('research-catalog');
  if (catalog) {
    const filters = ['year', 'field', 'architecture'].map(key => ({
      key, select: document.getElementById(`review-${key}`)
    }));
    const rows = [...catalog.querySelectorAll('tbody tr')];
    const applyFilters = () => {
      let count = 0;
      rows.forEach(row => {
        const visible = filters.every(({key, select}) => !select.value ||
          (key === 'field' ? row.dataset[key].split(' / ').includes(select.value) : row.dataset[key] === select.value));
        row.hidden = !visible;
        if (visible) count += 1;
      });
      document.getElementById('review-count').textContent = `${count} / ${rows.length}편 표시`;
    };
    document.querySelector('.review-filters').hidden = false;
    filters.forEach(({select}) => select.addEventListener('change', applyFilters));
    document.getElementById('review-reset').addEventListener('click', () => {
      filters.forEach(({select}) => { select.value = ''; });
      applyFilters();
    });
    applyFilters();
  }
  const dialog = document.getElementById('figure-dialog');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  let opener;
  document.querySelectorAll('a.figure-zoom').forEach(link => {
    link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      const img = link.querySelector('img');
      opener = link;
      const full = document.getElementById('figure-full');
      full.src = link.href;
      full.alt = img.alt;
      document.getElementById('figure-title').textContent = img.alt;
      document.getElementById('figure-original').href = link.href;
      dialog.showModal();
    });
  });
  dialog.addEventListener('close', () => { if (opener) opener.focus(); });
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
})();
