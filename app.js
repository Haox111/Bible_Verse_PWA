// ── State ─────────────────────────────────────────────────────────────────────
let allBooks  = [];   // book_meta.json
let chiun     = null; // chiun.json  (loaded lazily on first category switch)
let currentVerse = null;

// ── Boot ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
  setDateDisplay();
  emailjs.init(EMAILJS_CONFIG.publicKey);
  await loadToday();
  bindNav();
  bindEmail();
  registerSW();
});

// ── Date display ──────────────────────────────────────────────────────────────
function setDateDisplay() {
  const el = document.getElementById('date-display');
  el.textContent = new Date().toLocaleDateString('zh-Hant', {
    year: 'numeric', month: 'long', day: 'numeric', weekday: 'long',
  });
}

// ── Load today.json ───────────────────────────────────────────────────────────
async function loadToday() {
  try {
    const res = await fetch('data/today.json');
    if (!res.ok) throw new Error(res.statusText);
    const verse = await res.json();
    showVerse(verse);
  } catch {
    showError('無法加載今日經文，請稍後再試。');
  }
}

// ── Lazy-load chiun.json for category browsing ────────────────────────────────
async function ensureChiun() {
  if (chiun) return;
  const [bibleRes, metaRes] = await Promise.all([
    fetch('data/chiun.json'),
    fetch('data/book_meta.json'),
  ]);
  chiun     = await bibleRes.json();
  allBooks  = await metaRes.json();
}

// ── Render verse ──────────────────────────────────────────────────────────────
function showVerse(verse) {
  currentVerse = verse;
  document.getElementById('verse-text').textContent = `「${verse.text}」`;
  document.getElementById('verse-ref').textContent =
    `—— ${verse.book_zh}　${verse.chapter}：${verse.verse}`;
}

function showError(msg) {
  document.getElementById('verse-text').textContent = msg;
  document.getElementById('verse-ref').textContent  = '';
}

// ── Pick random verse from a category ────────────────────────────────────────
function pickFromCategory(testament) {
  const metaMap = Object.fromEntries(allBooks.map((m, i) => [i, m]));
  const bookPool = chiun.books
    .map((book, i) => ({ book, meta: metaMap[i] }))
    .filter(({ meta }) => {
      if (!meta) return false;
      if (testament === 'random') return true;
      if (testament === 'psalms')   return meta.name_en === 'Psalms';
      if (testament === 'proverbs') return meta.name_en === 'Proverbs';
      return meta.testament === testament;
    });

  if (!bookPool.length) { showError('該分類暫無經文。'); return; }

  // Weighted by verse count so longer books get fair representation
  const weights = bookPool.map(({ book }) =>
    book.chapters.reduce((sum, ch) => sum + ch.verses.length, 0)
  );
  const total = weights.reduce((a, b) => a + b, 0);
  let rand = Math.random() * total;
  let chosen;
  for (let i = 0; i < bookPool.length; i++) {
    rand -= weights[i];
    if (rand <= 0) { chosen = bookPool[i]; break; }
  }
  chosen = chosen || bookPool[bookPool.length - 1];

  const chapter = chosen.book.chapters[Math.floor(Math.random() * chosen.book.chapters.length)];
  const verse   = chapter.verses[Math.floor(Math.random() * chapter.verses.length)];

  showVerse({
    text:      verse.text.trim().replace(/\s+/g, ' '),
    book_zh:   chosen.meta.name_zh,
    book_en:   chosen.meta.name_en,
    chapter:   chapter.chapter,
    verse:     verse.verse,
    testament: chosen.meta.testament,
  });
}

// ── Bottom nav ────────────────────────────────────────────────────────────────
function bindNav() {
  document.querySelectorAll('.cat-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const testament = btn.dataset.testament;
      if (testament === 'today') { await loadToday(); return; }

      try {
        await ensureChiun();
        pickFromCategory(testament);
      } catch {
        showError('載入聖經數據失敗，請檢查網絡。');
      }
    });
  });
}

// ── Email modal ───────────────────────────────────────────────────────────────
function bindEmail() {
  document.getElementById('email-btn').addEventListener('click', () => {
    document.getElementById('email-modal').classList.remove('hidden');
    document.getElementById('email-input').focus();
  });
  document.getElementById('cancel-btn').addEventListener('click', closeModal);
  document.getElementById('send-btn').addEventListener('click', sendEmail);
  document.getElementById('email-modal').addEventListener('click', e => {
    if (e.target === e.currentTarget) closeModal();
  });
}

function closeModal() {
  document.getElementById('email-modal').classList.add('hidden');
  document.getElementById('send-status').textContent = '';
  document.getElementById('email-input').value = '';
}

async function sendEmail() {
  const email  = document.getElementById('email-input').value.trim();
  const status = document.getElementById('send-status');
  const sendBtn = document.getElementById('send-btn');

  if (!email || !email.includes('@')) {
    status.textContent = '請輸入有效的郵箱地址。'; return;
  }
  if (!currentVerse) { status.textContent = '經文尚未加載。'; return; }

  status.textContent = '發送中…';
  sendBtn.disabled = true;

  const { text, book_zh, chapter, verse } = currentVerse;
  const ref = `${book_zh} ${chapter}：${verse}`;

  try {
    await emailjs.send(EMAILJS_CONFIG.serviceId, EMAILJS_CONFIG.templateId, {
      to_email:  email,
      verse_text: text,
      verse_ref:  ref,
    });
    status.textContent = '✓ 已發送！請查收郵箱。';
    setTimeout(closeModal, 2000);
  } catch (err) {
    status.textContent = '發送失敗，請稍後再試。';
    console.error(err);
  } finally {
    sendBtn.disabled = false;
  }
}

// ── Service Worker ────────────────────────────────────────────────────────────
function registerSW() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('service-worker.js').catch(console.error);
  }
}
