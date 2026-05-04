const fs = require('fs').promises;
const path = require('path');

function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function formatTitle(filename) {
    return filename.replace(/\.html$/i, '').replace(/_/g, ' ');
}

(async () => {
    try {
        const webDir = path.resolve(__dirname, '..', 'Web');
        const entries = await fs.readdir(webDir, { withFileTypes: true });
        const htmlFiles = entries
            .filter(e => e.isFile() && e.name.toLowerCase().endsWith('.html') && e.name.toLowerCase() !== 'index.html')
            .map(e => e.name)
            .sort((a, b) => a.localeCompare(b, 'ko'));

        const listItems = htmlFiles.map((f, index) => {
            const title = escapeHtml(formatTitle(f));
            return `    <a class="resource-card" href="./${encodeURIComponent(f)}">
      <span class="card-index">${String(index + 1).padStart(2, '0')}</span>
      <span class="card-body">
        <strong>${title}</strong>
        <span>강의 자료 보기</span>
      </span>
      <span class="card-action" aria-hidden="true">열기</span>
    </a>`;
        }).join('\n');

        const html = `<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>자료 인덱스</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;800&display=swap');

    :root {
      --bg: #f4fbf8;
      --surface: #ffffff;
      --surface-soft: #edf8f3;
      --primary: #047857;
      --primary-dark: #064e3b;
      --secondary: #0e7490;
      --accent: #d97706;
      --border: #d9e7df;
      --text: #14231f;
      --muted: #64746f;
      --shadow: 0 18px 45px rgba(15, 45, 35, 0.10);
      --shadow-sm: 0 8px 22px rgba(15, 45, 35, 0.08);
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: 'Noto Sans KR', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
      background:
        linear-gradient(135deg, rgba(4,120,87,0.10), transparent 36%),
        linear-gradient(315deg, rgba(14,116,144,0.13), transparent 34%),
        var(--bg);
      color: var(--text);
      line-height: 1.7;
      min-height: 100vh;
    }

    .site-header {
      background: linear-gradient(135deg, #064e3b 0%, #047857 52%, #0e7490 100%);
      color: white;
      padding: 64px 24px 58px;
      position: relative;
      overflow: hidden;
    }

    .site-header::before {
      content: '';
      position: absolute;
      inset: 0;
      background-image:
        linear-gradient(rgba(255,255,255,0.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.07) 1px, transparent 1px);
      background-size: 34px 34px;
      -webkit-mask-image: linear-gradient(90deg, transparent, black 15%, black 85%, transparent);
      mask-image: linear-gradient(90deg, transparent, black 15%, black 85%, transparent);
    }

    .header-inner,
    .main {
      width: min(960px, calc(100% - 40px));
      margin: 0 auto;
      position: relative;
    }

    .eyebrow {
      display: inline-flex;
      align-items: center;
      min-height: 30px;
      padding: 4px 14px;
      border: 1px solid rgba(255,255,255,0.28);
      border-radius: 999px;
      background: rgba(255,255,255,0.14);
      color: rgba(255,255,255,0.9);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      margin-bottom: 18px;
    }

    h1 {
      margin: 0 0 14px;
      font-size: clamp(34px, 6vw, 58px);
      line-height: 1.12;
      letter-spacing: 0;
      font-weight: 800;
    }

    .lead {
      max-width: 640px;
      margin: 0;
      color: rgba(255,255,255,0.82);
      font-size: 17px;
    }

    .main {
      padding: 38px 0 56px;
    }

    .summary {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 20px;
      align-items: center;
      margin-bottom: 22px;
    }

    .summary h2 {
      margin: 0 0 4px;
      font-size: 22px;
      line-height: 1.3;
    }

    .summary p {
      margin: 0;
      color: var(--muted);
      font-size: 14px;
    }

    .count-badge {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 88px;
      height: 44px;
      padding: 0 16px;
      border-radius: 999px;
      background: var(--surface);
      border: 1px solid var(--border);
      box-shadow: var(--shadow-sm);
      color: var(--primary-dark);
      font-weight: 800;
      white-space: nowrap;
    }

    .resource-grid {
      display: grid;
      gap: 14px;
    }

    .resource-card {
      display: grid;
      grid-template-columns: auto minmax(0, 1fr) auto;
      gap: 18px;
      align-items: center;
      min-height: 96px;
      padding: 20px 22px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      color: inherit;
      text-decoration: none;
      box-shadow: var(--shadow-sm);
      transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    }

    .resource-card:hover {
      transform: translateY(-3px);
      border-color: rgba(4,120,87,0.36);
      box-shadow: var(--shadow);
    }

    .resource-card:focus-visible {
      outline: 3px solid rgba(14,116,144,0.35);
      outline-offset: 3px;
    }

    .card-index {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 46px;
      height: 46px;
      border-radius: 12px;
      background: linear-gradient(135deg, var(--surface-soft), #e0f2fe);
      color: var(--primary);
      font-size: 14px;
      font-weight: 800;
    }

    .card-body {
      min-width: 0;
    }

    .card-body strong {
      display: block;
      color: var(--text);
      font-size: 18px;
      line-height: 1.4;
      overflow-wrap: anywhere;
    }

    .card-body span {
      display: block;
      color: var(--muted);
      font-size: 13px;
      margin-top: 3px;
    }

    .card-action {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 58px;
      height: 34px;
      padding: 0 12px;
      border-radius: 8px;
      background: #fff7ed;
      color: var(--accent);
      font-size: 13px;
      font-weight: 700;
    }

    .empty-state {
      padding: 34px 24px;
      border: 1px dashed var(--border);
      border-radius: 14px;
      background: rgba(255,255,255,0.68);
      color: var(--muted);
      text-align: center;
    }

    .build-note {
      margin-top: 24px;
      padding-top: 18px;
      border-top: 1px solid var(--border);
      color: var(--muted);
      font-size: 13px;
    }

    @media (max-width: 640px) {
      .site-header { padding: 48px 20px 42px; }
      .header-inner,
      .main { width: min(100% - 28px, 960px); }
      .summary { grid-template-columns: 1fr; gap: 12px; }
      .count-badge { justify-self: start; }
      .resource-card {
        grid-template-columns: auto minmax(0, 1fr);
        padding: 18px;
      }
      .card-action {
        grid-column: 2;
        justify-self: start;
      }
    }
  </style>
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
      <div class="eyebrow">Data Analysis Workshop</div>
      <h1>웹 강의 자료</h1>
      <p class="lead">수업에서 사용하는 데이터 분석 자료를 한곳에 모았습니다. 새 HTML 자료가 추가되면 이 인덱스에도 자동으로 반영됩니다.</p>
    </div>
  </header>

  <main class="main">
    <section class="summary" aria-labelledby="resource-title">
      <div>
        <h2 id="resource-title">강의 자료 목록</h2>
        <p>파일명은 보기 좋게 정리해 표시하고, 링크는 실제 HTML 자료로 연결됩니다.</p>
      </div>
      <div class="count-badge">총 ${htmlFiles.length}개</div>
    </section>

    <section class="resource-grid" aria-label="강의 자료 링크">
${listItems || '      <div class="empty-state">아직 등록된 HTML 파일이 없습니다.</div>'}
    </section>

    <p class="build-note">이 파일은 <strong>npm run build</strong> 또는 Vercel 빌드 과정에서 자동 생성됩니다.</p>
  </main>
</body>
</html>
`;

        await fs.writeFile(path.join(webDir, 'index.html'), html, 'utf8');
        console.log('Web/index.html 생성됨. 항목:', htmlFiles);
    } catch (err) {
        console.error('인덱스 생성 중 오류:', err);
        process.exitCode = 1;
    }
})();
