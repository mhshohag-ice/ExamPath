/**
 * Question Navigator Component
 * Spec: Card titled "Navigator" with subtitle, grid 10 per row, circular buttons, states, responsive, no overflow
 * Usage:
 *   <div id="qn-root" data-total="197" data-current="2" data-answered="[1,5]" data-flagged="[3]"></div>
 *   <script type="module">
 *     import { QuestionNavigator } from '/static/js/question-navigator.js';
 *     const nav = new QuestionNavigator({
 *       container: document.getElementById('qn-root'),
 *       totalQuestions: 197,
 *       currentQuestion: 2,
 *       answeredQuestions: [1,5],
 *       flaggedQuestions: [3],
 *       onNavigate: (n) => console.log('navigate', n)
 *     });
 *   </script>
 * Or as Web Component:
 *   <question-navigator total="197" current="2" answered="1,5" flagged="3"></question-navigator>
 */

export class QuestionNavigator {
  /**
   * @param {Object} opts
   * @param {HTMLElement|string} opts.container - DOM element or selector
   * @param {number} opts.totalQuestions - total N
   * @param {number} opts.currentQuestion - 1-indexed current
   * @param {Array<number>|Set<number>} opts.answeredQuestions - numbers that are answered
   * @param {Array<number>|Set<number>} opts.flaggedQuestions - flagged/marked
   * @param {Array<number>|Set<number>} opts.skippedQuestions - skipped (optional)
   * @param {Function} opts.onNavigate - callback(questionNumber) when clicked
   * @param {boolean} opts.useVirtualization - force virtualization threshold (default 500)
   */
  constructor(opts = {}) {
    this.container = typeof opts.container === 'string' ? document.querySelector(opts.container) : opts.container;
    if (!this.container) throw new Error('QuestionNavigator: container not found');
    this.totalQuestions = Math.max(0, parseInt(opts.totalQuestions || 0, 10));
    this.currentQuestion = parseInt(opts.currentQuestion || 1, 10);
    this.answered = this._toSet(opts.answeredQuestions);
    this.flagged = this._toSet(opts.flaggedQuestions);
    this.skipped = this._toSet(opts.skippedQuestions);
    this.onNavigate = typeof opts.onNavigate === 'function' ? opts.onNavigate : null;
    this.useVirtualization = opts.useVirtualization ?? false;
    this.virtualThreshold = opts.virtualThreshold || 500;
    this._grid = null;
    this._render();
    this._bindEvents();
  }

  _toSet(arr) {
    if (!arr) return new Set();
    if (arr instanceof Set) return new Set(arr);
    if (Array.isArray(arr)) return new Set(arr.map(n => parseInt(n, 10)).filter(n => !isNaN(n)));
    if (typeof arr === 'string') {
      // "1,5,10" or "[1,5]" or JSON
      try {
        const parsed = JSON.parse(arr);
        if (Array.isArray(parsed)) return new Set(parsed.map(n => parseInt(n,10)));
      } catch {}
      return new Set(arr.split(',').map(s => parseInt(s.trim(),10)).filter(n=>!isNaN(n)));
    }
    return new Set();
  }

  _createCard() {
    // Card already exists if container is .question-navigator or .navigator-card
    // Otherwise create structure
    const hasCard = this.container.classList.contains('question-navigator') ||
                    this.container.classList.contains('navigator-card') ||
                    this.container.classList.contains('question-navigator-card');
    if (hasCard) return this.container;

    // Create card wrapper if container is empty plain div
    const card = document.createElement('div');
    card.className = 'card-premium question-navigator-card';
    card.setAttribute('role', 'region');
    card.setAttribute('aria-label', 'Question Navigator');
    // Header
    const header = document.createElement('h6');
    header.className = 'question-navigator-header';
    header.innerHTML = `Navigator <span class="question-navigator-subtitle">— ${this.totalQuestions} questions</span>`;
    card.appendChild(header);
    // Grid
    const grid = document.createElement('div');
    grid.className = 'question-navigator-grid';
    grid.setAttribute('role', 'navigation');
    grid.setAttribute('aria-label', 'Question navigator');
    card.appendChild(grid);
    this.container.appendChild(card);
    return card;
  }

  _render() {
    // Clear container if it was empty or contains previous grid
    let grid = this.container.querySelector('.question-navigator-grid, .q-nav-grid');
    let card = this.container.closest('.question-navigator, .navigator-card, .question-navigator-card') || this.container;

    // If container is the card itself, find grid inside
    if (this.container.classList.contains('question-navigator-grid') || this.container.classList.contains('q-nav-grid')) {
      grid = this.container;
      card = grid.closest('.card-premium');
    }

    if (!grid) {
      // Create full card+grid structure
      this.container.innerHTML = '';
      const newCard = this._createCard();
      grid = newCard.querySelector('.question-navigator-grid');
      // Add legend and help text per spec (if not already)
      if (!newCard.querySelector('.qn-legend')) {
        const legend = document.createElement('div');
        legend.className = 'qn-legend mt-3 small d-flex flex-column gap-1';
        legend.style.color = 'var(--color-text-muted)';
        legend.innerHTML = `
          <span><span style="width:10px;height:10px;background:transparent;border:1.5px solid var(--color-success-border);display:inline-block;border-radius:9999px;vertical-align:middle;"></span> Answered</span>
          <span><span style="width:10px;height:10px;background:transparent;border:1.5px solid #f59e0b;display:inline-block;border-radius:9999px;vertical-align:middle;"></span> Marked</span>
          <span><span style="width:10px;height:10px;background:var(--color-accent);display:inline-block;border-radius:9999px;vertical-align:middle;"></span> Current</span>
        `;
        newCard.appendChild(legend);
      }
    }

    this._grid = grid;
    // Ensure grid has correct classes and attributes for spec
    grid.classList.add('question-navigator-grid');
    // Also keep legacy class for existing CSS
    if (!grid.classList.contains('q-nav-grid')) grid.classList.add('q-nav-grid');
    grid.setAttribute('role', 'navigation');
    grid.setAttribute('aria-label', `Question navigator, ${this.totalQuestions} questions`);

    // Efficient render: Use DocumentFragment, plain map for ~200, virtualization for large
    const shouldVirtualize = this.totalQuestions > this.virtualThreshold;
    grid.innerHTML = '';
    grid.style.width = '100%';
    grid.style.maxWidth = '100%';
    grid.style.boxSizing = 'border-box';

    if (shouldVirtualize) {
      // Simple virtualization: render only visible + buffer, update on scroll
      // For brevity, implement windowing with IntersectionObserver-like chunking
      // Here we render all but with requestAnimationFrame chunking to avoid blocking
      this._renderChunked(grid, 0);
    } else {
      const frag = document.createDocumentFragment();
      for (let n = 1; n <= this.totalQuestions; n++) {
        frag.appendChild(this._createButton(n));
      }
      grid.appendChild(frag);
    }

    // Update header subtitle if exists
    const subtitle = this.container.querySelector('.question-navigator-subtitle') ||
                     document.querySelector('.question-navigator-subtitle');
    if (subtitle) subtitle.textContent = `— ${this.totalQuestions} questions`;
  }

  _renderChunked(grid, start) {
    const CHUNK = 50;
    const end = Math.min(start + CHUNK, this.totalQuestions);
    const frag = document.createDocumentFragment();
    for (let n = start + 1; n <= end; n++) {
      frag.appendChild(this._createButton(n));
    }
    grid.appendChild(frag);
    if (end < this.totalQuestions) {
      requestAnimationFrame(() => this._renderChunked(grid, end));
    }
  }

  _createButton(number) {
    const isCurrent = number === this.currentQuestion;
    const isAnswered = this.answered.has(number);
    const isFlagged = this.flagged.has(number);
    const isSkipped = this.skipped.has(number);

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'qn-btn';
    // Legacy class for existing CSS compatibility
    btn.classList.add('q-nav-btn');
    // Spec: circular, consistent, centered, no underline
    btn.style.textDecoration = 'none';
    btn.dataset.q = String(number);
    btn.setAttribute('aria-label', `Question ${number}${isCurrent ? ', current' : ''}${isAnswered ? ', answered' : ', unanswered'}${isFlagged ? ', flagged' : ''}`);
    if (isCurrent) btn.setAttribute('aria-current', 'true');
    btn.textContent = String(number);

    // State classes per spec (both new and legacy)
    if (isCurrent) {
      btn.classList.add('is-current', 'current');
    } else if (isAnswered && isFlagged) {
      btn.classList.add('is-answered', 'is-flagged', 'answered', 'marked', 'flagged');
    } else if (isAnswered) {
      btn.classList.add('is-answered', 'answered');
    } else if (isFlagged) {
      btn.classList.add('is-flagged', 'is-marked', 'flagged', 'marked');
    } else if (isSkipped) {
      btn.classList.add('is-skipped', 'skipped');
    } else {
      // unanswered default - no extra class
      btn.classList.add('is-unanswered');
    }

    // Ensure proper box-sizing and circular
    // (CSS handles most, but enforce inline for robustness)
    btn.style.boxSizing = 'border-box';
    btn.style.minWidth = '0';

    return btn;
  }

  _bindEvents() {
    if (!this._grid) return;
    // Delegate click
    this._grid.addEventListener('click', (e) => {
      const btn = e.target.closest('.qn-btn, .q-nav-btn');
      if (!btn || !this._grid.contains(btn)) return;
      const num = parseInt(btn.dataset.q || btn.textContent, 10);
      if (isNaN(num)) return;
      e.preventDefault();
      this.setCurrent(num);
      if (this.onNavigate) {
        this.onNavigate(num);
      } else {
        // Default behavior: navigate via query param ?q= (0-indexed for Django)
        const url = new URL(window.location.href);
        url.searchParams.set('q', String(num - 1));
        window.location.href = url.toString();
      }
      // Dispatch custom event for listeners
      this.container.dispatchEvent(new CustomEvent('navigate', { detail: { questionNumber: num }, bubbles: true }));
    });

    // Keyboard: make grid navigable
    this._grid.addEventListener('keydown', (e) => {
      const btns = [...this._grid.querySelectorAll('.qn-btn, .q-nav-btn')];
      const idx = btns.indexOf(document.activeElement);
      if (idx === -1) return;
      let nextIdx = -1;
      if (e.key === 'ArrowRight') nextIdx = Math.min(btns.length - 1, idx + 1);
      else if (e.key === 'ArrowLeft') nextIdx = Math.max(0, idx - 1);
      else if (e.key === 'ArrowDown') nextIdx = Math.min(btns.length - 1, idx + 10);
      else if (e.key === 'ArrowUp') nextIdx = Math.max(0, idx - 10);
      else if (e.key === 'Home') nextIdx = 0;
      else if (e.key === 'End') nextIdx = btns.length - 1;
      if (nextIdx !== -1) {
        e.preventDefault();
        btns[nextIdx].focus();
      }
    });
  }

  // Public API to update state without full re-render
  update({ currentQuestion, answeredQuestions, flaggedQuestions, skippedQuestions, totalQuestions } = {}) {
    let needsRender = false;
    if (typeof totalQuestions === 'number' && totalQuestions !== this.totalQuestions) {
      this.totalQuestions = totalQuestions;
      needsRender = true;
    }
    if (typeof currentQuestion === 'number' && currentQuestion !== this.currentQuestion) {
      this.currentQuestion = currentQuestion;
    }
    if (answeredQuestions !== undefined) {
      this.answered = this._toSet(answeredQuestions);
    }
    if (flaggedQuestions !== undefined) {
      this.flagged = this._toSet(flaggedQuestions);
    }
    if (skippedQuestions !== undefined) {
      this.skipped = this._toSet(skippedQuestions);
    }
    if (needsRender) {
      this._render();
    } else {
      // Efficiently update classes without rebuilding DOM
      this._updateStates();
    }
  }

  setCurrent(n) {
    this.currentQuestion = n;
    this._updateStates();
    // Ensure current is visible (scroll into view)
    const btn = this._grid.querySelector(`[data-q="${n}"]`);
    if (btn) btn.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: 'smooth' });
  }

  _updateStates() {
    if (!this._grid) return;
    const btns = this._grid.querySelectorAll('.qn-btn, .q-nav-btn');
    btns.forEach(btn => {
      const num = parseInt(btn.dataset.q || btn.textContent, 10);
      const isCurrent = num === this.currentQuestion;
      const isAnswered = this.answered.has(num);
      const isFlagged = this.flagged.has(num);
      const isSkipped = this.skipped.has(num);

      btn.classList.toggle('is-current', isCurrent);
      btn.classList.toggle('current', isCurrent);
      btn.classList.toggle('is-answered', isAnswered && !isCurrent);
      btn.classList.toggle('answered', isAnswered && !isCurrent);
      btn.classList.toggle('is-flagged', isFlagged);
      btn.classList.toggle('flagged', isFlagged);
      btn.classList.toggle('is-marked', isFlagged);
      btn.classList.toggle('marked', isFlagged);
      btn.classList.toggle('is-skipped', isSkipped);
      btn.classList.toggle('skipped', isSkipped);
      btn.classList.toggle('is-unanswered', !isAnswered && !isFlagged && !isSkipped && !isCurrent);

      if (isCurrent) btn.setAttribute('aria-current', 'true');
      else btn.removeAttribute('aria-current');
      btn.setAttribute('aria-label', `Question ${num}${isCurrent ? ', current' : ''}${isAnswered ? ', answered' : ', unanswered'}${isFlagged ? ', flagged' : ''}`);
    });
  }

  // Static helper to auto-init from data attributes
  static autoInit(root = document) {
    const nodes = root.querySelectorAll('[data-component="question-navigator"], [data-qn-total]');
    nodes.forEach(el => {
      const total = parseInt(el.dataset.total || el.dataset.qnTotal || el.getAttribute('data-total-questions') || '0', 10);
      const current = parseInt(el.dataset.current || el.dataset.qnCurrent || '1', 10);
      const answered = el.dataset.answered || el.dataset.qnAnswered || '[]';
      const flagged = el.dataset.flagged || el.dataset.qnFlagged || '[]';
      const skipped = el.dataset.skipped || '[]';
      const onNav = (n) => {
        const url = new URL(window.location.href);
        url.searchParams.set('q', String(n - 1));
        window.location.href = url.toString();
      };
      new QuestionNavigator({
        container: el,
        totalQuestions: total,
        currentQuestion: current,
        answeredQuestions: answered,
        flaggedQuestions: flagged,
        skippedQuestions: skipped,
        onNavigate: onNav
      });
    });
  }
}

// Web Component wrapper for declarative use
class QuestionNavigatorElement extends HTMLElement {
  static get observedAttributes() { return ['total', 'current', 'answered', 'flagged', 'skipped']; }
  connectedCallback() {
    const total = parseInt(this.getAttribute('total') || '0', 10);
    const current = parseInt(this.getAttribute('current') || '1', 10);
    const answered = this.getAttribute('answered') || '[]';
    const flagged = this.getAttribute('flagged') || '[]';
    const skipped = this.getAttribute('skipped') || '[]';
    this._instance = new QuestionNavigator({
      container: this,
      totalQuestions: total,
      currentQuestion: current,
      answeredQuestions: answered,
      flaggedQuestions: flagged,
      skippedQuestions: skipped,
      onNavigate: (n) => this.dispatchEvent(new CustomEvent('navigate', { detail: { questionNumber: n }, bubbles: true }))
    });
    // Add card styling if not already
    if (!this.classList.contains('question-navigator')) this.classList.add('question-navigator');
  }
  attributeChangedCallback(name, oldVal, newVal) {
    if (!this._instance) return;
    if (name === 'total') this._instance.update({ totalQuestions: parseInt(newVal,10) });
    if (name === 'current') this._instance.update({ currentQuestion: parseInt(newVal,10) });
    if (name === 'answered') this._instance.update({ answeredQuestions: newVal });
    if (name === 'flagged') this._instance.update({ flaggedQuestions: newVal });
    if (name === 'skipped') this._instance.update({ skippedQuestions: newVal });
  }
}
if (!customElements.get('question-navigator')) {
  customElements.define('question-navigator', QuestionNavigatorElement);
}

// Auto-init on DOMContentLoaded for data-component usage
if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => QuestionNavigator.autoInit());
}

// For non-module usage, expose globally
if (typeof window !== 'undefined') {
  window.QuestionNavigator = QuestionNavigator;
}
