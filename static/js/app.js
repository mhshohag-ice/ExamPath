// ExamPath App JS - Dark mode, HTMX, Alpine helpers, KaTeX, auto-save
(function() {
  // Theme
  const themeKey = 'uttoron-theme';
  function getPreferredTheme() {
    const stored = localStorage.getItem(themeKey);
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(themeKey, theme);
    const icon = document.getElementById('theme-icon');
    if (icon) icon.textContent = theme === 'dark' ? '☀️' : '🌙';
  }
  document.addEventListener('DOMContentLoaded', () => {
    setTheme(getPreferredTheme());
    document.getElementById('theme-toggle')?.addEventListener('click', () => {
      const cur = document.documentElement.getAttribute('data-theme');
      setTheme(cur === 'dark' ? 'light' : 'dark');
    });
    // KaTeX render
    if (window.renderMathInElement) {
      renderMathInElement(document.body, {
        delimiters: [
          {left: '\\(', right: '\\)', display: false},
          {left: '\\[', right: '\\]', display: true},
          {left: '$$', right: '$$', display: true},
          {left: '\\mathrm', right: '', display: false}
        ],
        throwOnError: false
      });
    }
    // Keyboard navigation for quiz
    document.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      const map = { 'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', '1': 'A', '2': 'B', '3': 'C', '4': 'D' };
      if (map[e.key.toLowerCase()]) {
        const btn = document.querySelector(`[data-choice="${map[e.key.toLowerCase()]}"]`);
        if (btn) { btn.click(); e.preventDefault(); }
      }
      if (e.key === 'ArrowLeft') document.getElementById('prev-btn')?.click();
      if (e.key === 'ArrowRight') document.getElementById('next-btn')?.click();
      if (e.key.toLowerCase() === 'm') document.getElementById('mark-btn')?.click();
    });
  });

  // Auto-save for quiz
  window.quizAutoSave = function(attemptId, questionId, choice) {
    fetch(`/quiz/${attemptId}/answer/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || getCookie('csrftoken')
      },
      body: JSON.stringify({question_id: questionId, choice: choice})
    }).catch(()=>{});
  };

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i=0;i<cookies.length;i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length+1)===(name+'=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length+1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // XP animation
  window.showXP = function(amount) {
    const el = document.createElement('div');
    el.textContent = `+${amount} XP`;
    el.style.cssText = 'position:fixed; top:20px; right:20px; background:#0f172a; color:white; padding:8px 16px; border-radius:9999px; font-weight:600; z-index:9999; animation: xp-pop 600ms ease-out forwards;';
    document.body.appendChild(el);
    setTimeout(()=>el.remove(), 1500);
  };
})();
