const assert = require('assert');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const cssPath = path.join(root, 'Web', 'assets', 'course-design-system.css');
const pages = {
  pandas: path.join(root, 'Web', '판다스_수업자료.html'),
  introFab: path.join(root, 'Web', '반도체_공정_데이터분석.html'),
  practicalFab: path.join(root, 'Web', '실전_반도체_공정_데이터분석_강의자료.html'),
};
const requested = process.argv.find(arg => arg.startsWith('--scope='));
const scope = requested ? requested.split('=')[1] : 'all';
const allowed = new Set(['foundation', 'pandas', 'toc', 'all']);
assert(allowed.has(scope), `지원하지 않는 scope: ${scope}`);

function read(file) {
  return fs.readFileSync(file, 'utf8');
}

function contains(source, value, label) {
  assert(source.includes(value), `${label}: ${value}`);
}

function verifyFoundation() {
  const css = read(cssPath);
  [
    '--course-canvas: #f8fafc',
    '--course-surface: #ffffff',
    '--course-primary: #2563eb',
    '--course-secondary: #06b6d4',
    '--course-tertiary: #7c3aed',
    '[data-course-theme="fabmetric"]',
    'inter, pretendard, "noto sans kr", system-ui, sans-serif',
  ].forEach(value => contains(css.toLowerCase(), value, '공통 CSS 누락'));
  assert(
    !/(^|\n)\s*(body|header|\.section|\.nav-bar)\s*\{/m.test(css),
    '테마 범위 밖의 전역 선택자가 있습니다.'
  );
}

function verifyPage(file, layout, expectedKorean) {
  const html = read(file);
  contains(html, '<link rel="stylesheet" href="./assets/course-design-system.css">', '스타일 링크 누락');
  contains(html, `data-course-theme="fabmetric"`, '테마 속성 누락');
  contains(html, `data-course-layout="${layout}"`, '레이아웃 속성 누락');
  contains(html, expectedKorean, 'UTF-8 한국어 본문 손상');
}

function verifyResponsiveContract() {
  const css = read(cssPath);
  [
    ':focus-visible',
    '@media (max-width: 767px)',
    '@media (prefers-reduced-motion: reduce)',
    '@media print',
    'overflow-x: auto',
  ].forEach(value => contains(css, value, '반응형 또는 접근성 규칙 누락'));
}

if (scope === 'foundation' || scope === 'all') verifyFoundation();
if (scope === 'pandas' || scope === 'all') {
  verifyPage(pages.pandas, 'tabs', '판다스로 배우는');
}
if (scope === 'toc' || scope === 'all') {
  verifyPage(pages.introFab, 'toc', '반도체 공정 데이터 분석');
  verifyPage(pages.practicalFab, 'toc', '실전 반도체 공정');
}
if (scope === 'all') verifyResponsiveContract();

console.log(`course design verification passed: ${scope}`);
