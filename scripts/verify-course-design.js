const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const cssPath = path.join(root, 'Web', 'assets', 'course-design-system.css');
const pages = {
  pandas: path.join(root, 'Web', '강좌', '01_판다스', '판다스_수업자료.html'),
  introFab: path.join(root, 'Web', '강좌', '02_반도체_공정_데이터분석', '반도체_공정_데이터분석.html'),
  practicalFab: path.join(root, 'Web', '강좌', '03_실전_반도체_공정_데이터분석', '실전_반도체_공정_데이터분석_강의자료.html'),
};
const requested = process.argv.find(arg => arg.startsWith('--scope='));
const scope = requested ? requested.split('=')[1] : 'all';
const allowed = new Set(['foundation', 'pandas', 'courses', 'all']);

if (!allowed.has(scope)) {
  throw new Error(`지원하지 않는 scope: ${scope}`);
}

const failures = [];

function read(file) {
  return fs.readFileSync(file, 'utf8');
}

function check(condition, message) {
  if (!condition) failures.push(message);
}

function contains(source, value, label) {
  check(source.includes(value), `${label}: ${value}`);
}

function stripCssComments(source) {
  let result = '';
  let quote = null;
  let escaped = false;

  for (let index = 0; index < source.length; index += 1) {
    const char = source[index];
    const next = source[index + 1];

    if (quote) {
      result += char;
      if (escaped) escaped = false;
      else if (char === '\\') escaped = true;
      else if (char === quote) quote = null;
      continue;
    }

    if (char === '"' || char === "'") {
      quote = char;
      result += char;
      continue;
    }

    if (char === '/' && next === '*') {
      index += 2;
      while (index < source.length && !(source[index] === '*' && source[index + 1] === '/')) {
        index += 1;
      }
      index += 1;
      result += ' ';
      continue;
    }

    result += char;
  }

  return result;
}

function findBlockEnd(source, openIndex) {
  let depth = 1;
  let quote = null;
  let escaped = false;

  for (let index = openIndex + 1; index < source.length; index += 1) {
    const char = source[index];

    if (quote) {
      if (escaped) escaped = false;
      else if (char === '\\') escaped = true;
      else if (char === quote) quote = null;
      continue;
    }

    if (char === '"' || char === "'") quote = char;
    else if (char === '{') depth += 1;
    else if (char === '}') {
      depth -= 1;
      if (depth === 0) return index;
    }
  }

  throw new Error('공통 CSS의 중괄호가 닫히지 않았습니다.');
}

function splitSelectorList(prelude) {
  const selectors = [];
  let start = 0;
  let parentheses = 0;
  let brackets = 0;
  let quote = null;
  let escaped = false;

  for (let index = 0; index < prelude.length; index += 1) {
    const char = prelude[index];

    if (quote) {
      if (escaped) escaped = false;
      else if (char === '\\') escaped = true;
      else if (char === quote) quote = null;
      continue;
    }

    if (char === '"' || char === "'") quote = char;
    else if (char === '(') parentheses += 1;
    else if (char === ')') parentheses -= 1;
    else if (char === '[') brackets += 1;
    else if (char === ']') brackets -= 1;
    else if (char === ',' && parentheses === 0 && brackets === 0) {
      selectors.push(prelude.slice(start, index).trim());
      start = index + 1;
    }
  }

  selectors.push(prelude.slice(start).trim());
  return selectors.filter(Boolean);
}

function collectStyleRules(source) {
  const css = stripCssComments(source);
  const rules = [];
  const declarationAtRules = new Set([
    'counter-style',
    'font-face',
    'font-feature-values',
    'page',
    'property',
  ]);

  function walk(start, end) {
    let cursor = start;

    while (cursor < end) {
      while (cursor < end && /\s/.test(css[cursor])) cursor += 1;
      if (cursor >= end) break;

      let index = cursor;
      let parentheses = 0;
      let brackets = 0;
      let quote = null;
      let escaped = false;

      for (; index < end; index += 1) {
        const char = css[index];

        if (quote) {
          if (escaped) escaped = false;
          else if (char === '\\') escaped = true;
          else if (char === quote) quote = null;
          continue;
        }

        if (char === '"' || char === "'") quote = char;
        else if (char === '(') parentheses += 1;
        else if (char === ')') parentheses -= 1;
        else if (char === '[') brackets += 1;
        else if (char === ']') brackets -= 1;
        else if ((char === '{' || char === ';') && parentheses === 0 && brackets === 0) break;
      }

      if (index >= end) break;
      if (css[index] === ';') {
        cursor = index + 1;
        continue;
      }

      const prelude = css.slice(cursor, index).trim();
      const closeIndex = findBlockEnd(css, index);
      const body = css.slice(index + 1, closeIndex);

      if (prelude.startsWith('@')) {
        const match = prelude.match(/^@(?:-[\w]+-)?([\w-]+)/);
        const atRuleName = match ? match[1].toLowerCase() : '';
        const containsDeclarations = declarationAtRules.has(atRuleName) || atRuleName === 'keyframes';
        if (!containsDeclarations) walk(index + 1, closeIndex);
      } else {
        rules.push({ prelude, selectors: splitSelectorList(prelude), body });
      }

      cursor = closeIndex + 1;
    }
  }

  walk(0, css.length);
  return rules;
}

function normalizeCssFunction(value) {
  return value
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .replace(/\s*,\s*/g, ', ')
    .trim();
}

function collectGradientFunctions(source) {
  const css = stripCssComments(source);
  const gradients = [];
  const pattern = /(?:repeating-)?(?:linear|radial|conic)-gradient\s*\(/gi;
  let match;

  while ((match = pattern.exec(css)) !== null) {
    let depth = 1;
    let quote = null;
    let escaped = false;
    let index = pattern.lastIndex;

    for (; index < css.length && depth > 0; index += 1) {
      const char = css[index];
      if (quote) {
        if (escaped) escaped = false;
        else if (char === '\\') escaped = true;
        else if (char === quote) quote = null;
      } else if (char === '"' || char === "'") quote = char;
      else if (char === '(') depth += 1;
      else if (char === ')') depth -= 1;
    }

    gradients.push(normalizeCssFunction(css.slice(match.index, index)));
    pattern.lastIndex = index;
  }

  return gradients;
}

function getRule(rules, selector) {
  return rules.find(rule => rule.selectors.some(item => item.replace(/\s+/g, ' ') === selector));
}

function verifyVerifierGuards() {
  const selectorProbe = `
    @media screen {
      [data-course-theme="fabmetric"] .safe { color: black; }
    }
    @supports (display: grid) {
      body, [data-course-theme="fabmetric"] .mixed { display: grid; }
    }
    @keyframes pulse {
      from { opacity: 0; }
      to { opacity: 1; }
    }
  `;
  const probeSelectors = collectStyleRules(selectorProbe).flatMap(rule => rule.selectors);
  check(probeSelectors.includes('body'), '내부 검증 실패: 중첩된 비테마 선택자를 찾지 못했습니다.');
  check(!probeSelectors.includes('from') && !probeSelectors.includes('to'), '내부 검증 실패: keyframe 단계를 CSS 선택자로 처리했습니다.');

  const gradientProbe = 'a { background: radial-gradient(circle, red, blue); }';
  check(
    collectGradientFunctions(gradientProbe)[0] === 'radial-gradient(circle, red, blue)',
    '내부 검증 실패: 금지 gradient를 찾지 못했습니다.'
  );
}

function verifyFoundation() {
  const css = read(cssPath);
  const cssLower = css.toLowerCase();
  verifyVerifierGuards();
  const expectedTokens = {
    '--course-canvas': '#f8fafc',
    '--course-surface': '#ffffff',
    '--course-surface-low': '#f1f5f9',
    '--course-text': '#0f172a',
    '--course-muted': '#64748b',
    '--course-border': '#e2e8f0',
    '--course-primary': '#2563eb',
    '--course-secondary': '#06b6d4',
    '--course-tertiary': '#7c3aed',
    '--course-success': '#10b981',
    '--course-warning': '#f59e0b',
    '--course-error': '#ef4444',
    '--course-focus': '#1d4ed8',
    '--course-focus-on-dark': '#93c5fd',
    '--course-code-comment': '#94a3b8',
    '--course-output-label': '#475569',
  };

  for (const [token, value] of Object.entries(expectedTokens)) {
    check(
      new RegExp(`${token.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\s*:\\s*${value}\\s*;`, 'i').test(css),
      `디자인 토큰 누락 또는 값 불일치: ${token}: ${value}`
    );
  }

  contains(cssLower, 'inter, pretendard, "noto sans kr", system-ui, sans-serif', '공통 글꼴 스택 누락');

  const rules = collectStyleRules(css);
  const scopePattern = /^\[data-course-theme\s*=\s*(["'])fabmetric\1\]/i;
  const unscoped = rules.flatMap(rule => rule.selectors.filter(selector => !scopePattern.test(selector)));
  check(unscoped.length === 0, `테마 범위 밖의 CSS 선택자: ${unscoped.join(' | ')}`);

  const allowedGradients = new Set([
    'linear-gradient(var(--course-border) 1px, transparent 1px)',
    'linear-gradient(90deg, var(--course-border) 1px, transparent 1px)',
  ]);
  const gradients = collectGradientFunctions(css);
  const invalidGradients = gradients.filter(value => !allowedGradients.has(value));
  check(invalidGradients.length === 0, `1px 기술 격자 외 gradient 사용: ${invalidGradients.join(' | ')}`);
  for (const gridGradient of allowedGradients) {
    check(gradients.includes(gridGradient), `기술 격자 gradient 누락: ${gridGradient}`);
  }
}

function verifyPage(file, layout, expectedKorean, cssHref = './assets/course-design-system.css') {
  const html = read(file);
  contains(html, `<link rel="stylesheet" href="${cssHref}">`, '스타일 링크 누락');
  check(fs.existsSync(path.resolve(path.dirname(file), cssHref)), `스타일 파일 경로 오류: ${cssHref}`);
  contains(html, 'data-course-theme="fabmetric"', '테마 속성 누락');
  contains(html, `data-course-layout="${layout}"`, '레이아웃 속성 누락');
  contains(html, expectedKorean, 'UTF-8 한국어 본문 손상');
  return html;
}

// 강좌 탭형 페이지 공통 검사 (01·02·03 강좌가 같은 구조를 따르는지)
function verifyTabsPage(name, file, expectedKorean, tabCount) {
  const html = verifyPage(file, 'tabs', expectedKorean, '../../assets/course-design-system.css');
  contains(html, '<link rel="stylesheet" href="../../assets/course-tabs.css">', `${name} 공통 탭 스타일 링크 누락`);
  check(fs.existsSync(path.resolve(path.dirname(file), '../../assets/course-tabs.css')), `${name} 공통 탭 스타일 파일 없음`);
  const css = read(cssPath);
  const rules = collectStyleRules(css);
  const buttonTabs = [...html.matchAll(/<button\b[^>]*class="[^"]*\bnav-tab\b[^"]*"[^>]*>/g)].map(match => match[0]);

  check(/<div\s+class="nav-inner"\s+role="tablist"\s+aria-label="차시 선택">/.test(html), `${name} 탭 목록의 role="tablist" 또는 레이블 누락`);
  check(buttonTabs.length === tabCount, `${name} button 탭 수 불일치: ${buttonTabs.length}/${tabCount}`);
  buttonTabs.forEach((tag, index) => {
    const number = index + 1;
    check(/type="button"/.test(tag), `${name} ${number}번 탭 type="button" 누락`);
    check(/role="tab"/.test(tag), `${name} ${number}번 탭 role="tab" 누락`);
    check(new RegExp(`id="tab-${number}"`).test(tag), `${name} ${number}번 탭 id 누락`);
    check(new RegExp(`aria-controls="session-${number}"`).test(tag), `${name} ${number}번 탭 aria-controls 누락`);
    check(/aria-selected="(?:true|false)"/.test(tag), `${name} ${number}번 탭 aria-selected 누락`);
    check(/tabindex="(?:0|-1)"/.test(tag), `${name} ${number}번 탭 roving tabindex 누락`);
  });

  for (let number = 1; number <= tabCount; number += 1) {
    const panelPattern = new RegExp(`<section\\s+class="[^"]*session-pane[^"]*"\\s+id="session-${number}"[^>]*role="tabpanel"[^>]*aria-labelledby="tab-${number}"`);
    check(panelPattern.test(html), `${name} ${number}번 패널의 tabpanel 관계 누락`);
  }

  const notebookLinks = [...html.matchAll(/<a class="notebook-link" href="([^"]+\.ipynb)"/g)].map(match => match[1]);
  check(notebookLinks.length === tabCount, `${name} 탭별 실습 노트북 링크 수 불일치: ${notebookLinks.length}/${tabCount}`);
  notebookLinks.forEach(href => {
    check(fs.existsSync(path.resolve(path.dirname(file), href)), `${name} 실습 노트북 파일 없음: ${href}`);
  });

  ['ArrowLeft', 'ArrowRight', 'Home', 'End', 'Enter'].forEach(key => {
    contains(html, `'${key}'`, `${name} 탭 키보드 처리 누락`);
  });
  check(/event\.key\s*===\s*' '\s*\|\|\s*event\.key\s*===\s*'Spacebar'/.test(html), `${name} 탭 Space 키 처리 누락`);
  contains(html, "matchMedia('(prefers-reduced-motion: reduce)')", `${name} reduced-motion 감지 누락`);
  check(/behavior:\s*reduceMotion\s*\?\s*'auto'\s*:\s*'smooth'/.test(html), `${name} scrollTo의 reduced-motion 분기 누락`);
  contains(html, "setAttribute('aria-selected'", `${name} showSession ARIA 상태 동기화 누락`);
  contains(html, "setAttribute('tabindex'", `${name} showSession roving tabindex 동기화 누락`);
  contains(html, '.hidden =', `${name} showSession 패널 hidden 상태 동기화 누락`);

  const h1 = getRule(rules, '[data-course-theme="fabmetric"][data-course-layout="tabs"] .site-header h1');
  check(Boolean(h1), `${name} 데스크톱 H1 전용 규칙 누락`);
  if (h1) {
    check(/font-size:\s*36px\s*;/.test(h1.body), `${name} 데스크톱 H1 36px 고정값 누락`);
    check(/line-height:\s*1\.22\s*;/.test(h1.body), `${name} 데스크톱 H1 line-height 누락`);
    check(/letter-spacing:\s*0\s*;/.test(h1.body), `${name} 데스크톱 H1 letter-spacing: 0 누락`);
  }

  const pseudo = getRule(rules, '[data-course-theme="fabmetric"][data-course-layout="tabs"] .site-header::before');
  check(Boolean(pseudo) && /display:\s*none\s*;/.test(pseudo.body), `${name} legacy .site-header::before 비활성화 누락`);

  const focus = getRule(rules, '[data-course-theme="fabmetric"] :is(a, button):focus-visible');
  check(Boolean(focus) && /outline:\s*3px\s+solid\s+var\(--course-focus\)\s*;/.test(focus.body), '불투명 고대비 focus-visible outline 누락');

  const comment = getRule(rules, '[data-course-theme="fabmetric"][data-course-layout="tabs"] :is(pre .cmt, pre .cm)');
  check(Boolean(comment) && /color:\s*var\(--course-code-comment\)\s*;/.test(comment.body), `${name} 코드 주석 대비 토큰 적용 누락`);
  const outputLabel = getRule(rules, '[data-course-theme="fabmetric"][data-course-layout="tabs"] .output-label');
  check(Boolean(outputLabel) && /color:\s*var\(--course-output-label\)\s*;/.test(outputLabel.body), `${name} output-label 대비 토큰 적용 누락`);
  return html;
}

// 강좌 폴더 페이지의 실습 노트북·데이터 링크가 실제 파일을 가리키는지 확인
function verifyLocalLinks(file, html, expectedNotebooks) {
  const hrefs = [...html.matchAll(/href="(\.\/실습\/[^"]+)"/g)].map(match => match[1]);
  const notebooks = new Set(hrefs.filter(href => href.endsWith('.ipynb')));
  check(notebooks.size === expectedNotebooks, `${path.basename(file)} 실습 노트북 링크 수 불일치: ${notebooks.size}/${expectedNotebooks}`);
  hrefs.forEach(href => {
    check(fs.existsSync(path.resolve(path.dirname(file), href)), `${path.basename(file)} 링크 대상 파일 없음: ${href}`);
  });
}

function verifyPandas() {
  verifyTabsPage('Pandas', pages.pandas, '판다스로 배우는', 5);
}

function verifyCourses() {
  const introFab = verifyTabsPage('반도체 공정', pages.introFab, '반도체 공정', 6);
  verifyLocalLinks(pages.introFab, introFab, 6);
  const practicalFab = verifyTabsPage('실전 반도체', pages.practicalFab, '실전 반도체 공정', 6);
  verifyLocalLinks(pages.practicalFab, practicalFab, 6);
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
if (scope === 'pandas' || scope === 'all') verifyPandas();
if (scope === 'courses' || scope === 'all') verifyCourses();
if (scope === 'all') verifyResponsiveContract();

if (failures.length > 0) {
  console.error(`course design verification failed: ${scope}`);
  failures.forEach(message => console.error(`- ${message}`));
  process.exit(1);
}

console.log(`course design verification passed: ${scope}`);
