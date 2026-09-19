# Course Design System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply the FabMetric Telemetry visual system to the 01, 05, and 06 course pages through one reusable, scoped CSS design system without changing lesson content or existing interactions.

**Architecture:** Add one shared stylesheet scoped by `data-course-theme="fabmetric"`, with separate adapters selected by `data-course-layout="tabs"` and `data-course-layout="toc"`. Add a dependency-free Node verifier that checks the theme contract and page integration before browser-based responsive and interaction verification.

**Tech Stack:** Static HTML, CSS custom properties, vanilla JavaScript, Node.js 14+, PowerShell, local HTTP server, browser responsive testing.

**Spec:** `docs/superpowers/specs/2026-09-19-course-design-system-design.md`

## Global Constraints

- Preserve Korean filenames, headings, examples, instructional tone, example code, and data files.
- Apply the new theme only to `Web/판다스_수업자료.html`, `Web/반도체_공정_데이터분석.html`, and `Web/실전_반도체_공정_데이터분석_강의자료.html`.
- Do not modify or commit `stitch-reference/`.
- Do not introduce Tailwind, a JavaScript framework, or any new package dependency.
- Keep the existing tab switching, table-of-contents anchors, copy buttons, and `IntersectionObserver` logic unchanged.
- Scope every shared rule below `[data-course-theme="fabmetric"]` so other pages cannot inherit it.
- Use `#F8FAFC`, `#FFFFFF`, `#F1F5F9`, `#0F172A`, `#64748B`, `#E2E8F0`, `#2563EB`, `#06B6D4`, `#7C3AED`, `#10B981`, `#F59E0B`, and `#EF4444` for the documented semantic roles.
- Use card and control radii of 8px or less, 1px borders for hierarchy, and no decorative gradient or radial-orb backgrounds.
- Run `npm run build` after all `Web/` changes and keep `Web/index.html` consistent with `Web/order.txt`.

## Review Focus

- A shared selector leaking into unthemed pages: only elements under the FabMetric data attribute may change.
- A missing stylesheet or wrong relative path: all three pages must resolve `./assets/course-design-system.css` from `Web/`.
- A mobile-wide table or code sample widening the entire document: only `.tbl-wrap`, `.table-wrap`, `pre`, or the code container may scroll horizontally.
- Existing controls losing behavior after visual changes: all three Pandas tabs, TOC anchors, copy buttons, and TOC active states must still work.
- External font failure: system fallbacks must render readable Korean without changing fixed control dimensions or causing overlap.

---

### Task 1: Theme Contract Verifier and Shared Foundation

**Files:**
- Create: `scripts/verify-course-design.js`
- Create: `Web/assets/course-design-system.css`
- Modify: `package.json:5-7`

**Interfaces:**
- Consumes: the final target page paths and the design tokens from the approved spec.
- Produces: `npm run verify:course-design -- --scope=<foundation|pandas|toc|all>` and the scoped CSS variables consumed by both page adapters.

- [ ] **Step 1: Write the structural verifier before creating the stylesheet**

Create `scripts/verify-course-design.js` with dependency-free assertions and scope selection:

```js
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
```

- [ ] **Step 2: Add the verifier command**

Change the `scripts` object in `package.json` to:

```json
"scripts": {
  "build": "node scripts/generate-index.js",
  "verify:course-design": "node scripts/verify-course-design.js"
}
```

- [ ] **Step 3: Run the foundation check and confirm the missing stylesheet failure**

Run:

```powershell
npm run verify:course-design -- --scope=foundation
```

Expected: FAIL with `ENOENT` for `Web/assets/course-design-system.css`.

- [ ] **Step 4: Create the shared token and reset layer**

Create `Web/assets/course-design-system.css` with this foundation:

```css
/*
 * Usage:
 * <link rel="stylesheet" href="./assets/course-design-system.css">
 * <body data-course-theme="fabmetric" data-course-layout="tabs|toc">
 */
[data-course-theme="fabmetric"] {
  --course-canvas: #f8fafc;
  --course-surface: #ffffff;
  --course-surface-low: #f1f5f9;
  --course-text: #0f172a;
  --course-muted: #64748b;
  --course-border: #e2e8f0;
  --course-primary: #2563eb;
  --course-secondary: #06b6d4;
  --course-tertiary: #7c3aed;
  --course-success: #10b981;
  --course-warning: #f59e0b;
  --course-error: #ef4444;
  --course-code: #0f172a;
  --course-code-toolbar: #1e293b;
  --course-shadow: 0 1px 3px rgba(15, 23, 42, 0.05), 0 1px 2px rgba(15, 23, 42, 0.03);
  background: var(--course-canvas);
  color: var(--course-text);
  font-family: Inter, Pretendard, "Noto Sans KR", system-ui, sans-serif;
  font-feature-settings: "tnum" 1, "cv05" 1;
}

[data-course-theme="fabmetric"] *,
[data-course-theme="fabmetric"] *::before,
[data-course-theme="fabmetric"] *::after {
  box-sizing: border-box;
}

[data-course-theme="fabmetric"] :is(button, a) {
  -webkit-tap-highlight-color: transparent;
}
```

- [ ] **Step 5: Run the foundation verification**

Run:

```powershell
npm run verify:course-design -- --scope=foundation
```

Expected: PASS with `course design verification passed: foundation`.

- [ ] **Step 6: Commit the verifier and foundation**

```powershell
git add package.json scripts/verify-course-design.js Web/assets/course-design-system.css
git commit -m "강좌 디자인 시스템 기반 추가"
```

### Task 2: Pandas Tabs Page Adapter

**Files:**
- Modify: `Web/판다스_수업자료.html:518-520`
- Modify: `Web/assets/course-design-system.css`

**Interfaces:**
- Consumes: the foundation variables and `data-course-layout="tabs"` contract from Task 1.
- Produces: a themed Pandas page whose existing `showSession(num, tab)` and `copyCode(btn)` functions remain unchanged.

- [ ] **Step 1: Run the Pandas integration check before changing the page**

Run:

```powershell
npm run verify:course-design -- --scope=pandas
```

Expected: FAIL with `스타일 링크 누락`.

- [ ] **Step 2: Opt the Pandas page into the theme**

Immediately after the existing closing `</style>`, add:

```html
<link rel="stylesheet" href="./assets/course-design-system.css">
```

Replace `<body>` with:

```html
<body data-course-theme="fabmetric" data-course-layout="tabs">
```

- [ ] **Step 3: Add the tabs adapter using existing class names**

Append rules scoped by `[data-course-layout="tabs"]` that implement these exact mappings:

```css
[data-course-theme="fabmetric"][data-course-layout="tabs"] .site-header {
  padding: 48px 24px 40px;
  color: var(--course-text);
  background-color: var(--course-surface);
  background-image: linear-gradient(var(--course-border) 1px, transparent 1px),
                    linear-gradient(90deg, var(--course-border) 1px, transparent 1px);
  background-size: 32px 32px;
  border-top: 4px solid var(--course-primary);
  border-bottom: 1px solid var(--course-border);
}

[data-course-theme="fabmetric"][data-course-layout="tabs"] .site-header::before {
  background: linear-gradient(90deg, rgba(248, 250, 252, 0.96), rgba(248, 250, 252, 0.72));
}

[data-course-theme="fabmetric"][data-course-layout="tabs"] .header-tag,
[data-course-theme="fabmetric"][data-course-layout="tabs"] .nav-tab .session-num {
  border: 1px solid #bfdbfe;
  border-radius: 6px;
  background: #eff6ff;
  color: var(--course-primary);
}

[data-course-theme="fabmetric"][data-course-layout="tabs"] .nav-bar {
  top: 0;
  background: rgba(255, 255, 255, 0.96);
  border-color: var(--course-border);
  box-shadow: var(--course-shadow);
}

[data-course-theme="fabmetric"][data-course-layout="tabs"] .nav-tab {
  min-height: 44px;
  color: var(--course-muted);
  border-bottom-color: transparent;
}

[data-course-theme="fabmetric"][data-course-layout="tabs"] .nav-tab.active {
  color: var(--course-primary);
  background: #eff6ff;
  border-bottom-color: var(--course-primary);
}

[data-course-theme="fabmetric"][data-course-layout="tabs"] :is(.session-header, .content-card) {
  border: 1px solid var(--course-border);
  border-radius: 8px;
  background: var(--course-surface);
  box-shadow: var(--course-shadow);
}

[data-course-theme="fabmetric"][data-course-layout="tabs"] .objectives {
  border: 1px solid #bae6fd;
  border-left: 3px solid var(--course-secondary);
  border-radius: 8px;
  background: #ecfeff;
}
```

Add the remaining existing components with explicit token mappings:

```css
[data-course-theme="fabmetric"][data-course-layout="tabs"] .section-num {
  border-radius: 6px;
  background: var(--course-primary);
  color: #fff;
}

[data-course-theme="fabmetric"][data-course-layout="tabs"] :is(.concept-box, .analogy, .tip-box, .info, .success, .quiz-section) {
  border: 1px solid var(--course-border);
  border-radius: 8px;
  background: var(--course-surface-low);
  box-shadow: none;
}

[data-course-theme="fabmetric"][data-course-layout="tabs"] .tip-box {
  border-left: 3px solid var(--course-secondary);
  background: #ecfeff;
}

[data-course-theme="fabmetric"][data-course-layout="tabs"] .info {
  border-left: 3px solid var(--course-primary);
  background: #eff6ff;
}

[data-course-theme="fabmetric"][data-course-layout="tabs"] .success {
  border-left: 3px solid var(--course-success);
  background: #ecfdf5;
}

[data-course-theme="fabmetric"][data-course-layout="tabs"] :is(.code-wrap, .code-block) {
  border: 1px solid #334155;
  border-radius: 8px;
  background: var(--course-code);
  box-shadow: none;
}

[data-course-theme="fabmetric"][data-course-layout="tabs"] .code-header {
  background: var(--course-code-toolbar);
  border-color: #334155;
}

[data-course-theme="fabmetric"][data-course-layout="tabs"] pre {
  background: var(--course-code);
  color: #e2e8f0;
  font-family: "JetBrains Mono", Consolas, monospace;
}

[data-course-theme="fabmetric"][data-course-layout="tabs"] .copy-btn {
  min-height: 36px;
  border: 1px solid #475569;
  border-radius: 6px;
  background: #334155;
  color: #f8fafc;
}

[data-course-theme="fabmetric"][data-course-layout="tabs"] :is(.api-table, table) {
  border-color: var(--course-border);
  background: var(--course-surface);
}

[data-course-theme="fabmetric"][data-course-layout="tabs"] :is(.api-table, table) th {
  background: var(--course-surface-low);
  color: var(--course-muted);
}

[data-course-theme="fabmetric"][data-course-layout="tabs"] [id^="ai-"] {
  border: 1px solid var(--course-border) !important;
  border-left: 3px solid var(--course-tertiary) !important;
  border-radius: 8px !important;
  background: #faf5ff !important;
  box-shadow: none !important;
}

[data-course-theme="fabmetric"][data-course-layout="tabs"] .site-footer {
  border-top: 1px solid var(--course-border);
  background: var(--course-code);
  color: #cbd5e1;
}
```

- [ ] **Step 4: Run the Pandas structural verification**

Run:

```powershell
npm run verify:course-design -- --scope=pandas
```

Expected: PASS with `course design verification passed: pandas`.

- [ ] **Step 5: Verify tab and copy interactions at desktop width**

Run the site:

```powershell
python -m http.server 4173 --directory Web
```

Open `http://localhost:4173/%ED%8C%90%EB%8B%A4%EC%8A%A4_%EC%88%98%EC%97%85%EC%9E%90%EB%A3%8C.html` at 1440x900. Click all three `.nav-tab` controls and verify exactly one `.session-pane` is visible after each click. Click the first `.copy-btn` and verify its text changes to the existing copied state without a console error.

- [ ] **Step 6: Commit the Pandas adapter**

```powershell
git add Web/판다스_수업자료.html Web/assets/course-design-system.css
git commit -m "판다스 강좌에 공통 디자인 적용"
```

### Task 3: Semiconductor TOC Page Adapter

**Files:**
- Modify: `Web/반도체_공정_데이터분석.html:467-469`
- Modify: `Web/실전_반도체_공정_데이터분석_강의자료.html:388-390`
- Modify: `Web/assets/course-design-system.css`

**Interfaces:**
- Consumes: the foundation variables and `data-course-layout="toc"` contract from Task 1.
- Produces: matching 05 and 06 course layouts while retaining each page's existing TOC links, section IDs, copy code, and scroll observer.

- [ ] **Step 1: Run the TOC integration check before changing either page**

Run:

```powershell
npm run verify:course-design -- --scope=toc
```

Expected: FAIL with `스타일 링크 누락` for the first TOC page.

- [ ] **Step 2: Opt both TOC pages into the shared theme**

In each file, add this immediately after the existing closing `</style>`:

```html
<link rel="stylesheet" href="./assets/course-design-system.css">
```

Replace each `<body>` with:

```html
<body data-course-theme="fabmetric" data-course-layout="toc">
```

- [ ] **Step 3: Add the shared TOC adapter**

Append these core mappings:

```css
[data-course-theme="fabmetric"][data-course-layout="toc"] header {
  padding: 48px 24px 40px;
  color: var(--course-text);
  background-color: var(--course-surface);
  background-image: linear-gradient(var(--course-border) 1px, transparent 1px),
                    linear-gradient(90deg, var(--course-border) 1px, transparent 1px);
  background-size: 32px 32px;
  border-top: 4px solid var(--course-primary);
  border-bottom: 1px solid var(--course-border);
}

[data-course-theme="fabmetric"][data-course-layout="toc"] header::before,
[data-course-theme="fabmetric"][data-course-layout="toc"] header::after {
  display: none;
}

[data-course-theme="fabmetric"][data-course-layout="toc"] h1 {
  max-width: 760px;
  margin-bottom: 12px;
  color: var(--course-text);
  background: none;
  font-family: Inter, Pretendard, "Noto Sans KR", system-ui, sans-serif;
  font-size: 36px;
  line-height: 1.22;
  letter-spacing: 0;
  -webkit-text-fill-color: currentColor;
}

[data-course-theme="fabmetric"][data-course-layout="toc"] .layout {
  max-width: 1280px;
  gap: 24px;
  padding: 32px;
}

[data-course-theme="fabmetric"][data-course-layout="toc"] .toc {
  width: 240px;
  top: 16px;
  border: 1px solid var(--course-border);
  border-radius: 8px;
  background: var(--course-surface);
  box-shadow: var(--course-shadow);
}

[data-course-theme="fabmetric"][data-course-layout="toc"] .toc a:hover,
[data-course-theme="fabmetric"][data-course-layout="toc"] .toc a.active {
  color: var(--course-primary);
  border-left-color: var(--course-primary);
  background: #eff6ff;
}

[data-course-theme="fabmetric"][data-course-layout="toc"] .section {
  border: 1px solid var(--course-border);
  border-radius: 8px;
  background: var(--course-surface);
  box-shadow: var(--course-shadow);
}

[data-course-theme="fabmetric"][data-course-layout="toc"] .subsection {
  border: 0;
  border-top: 1px solid var(--course-border);
  border-radius: 0;
  background: transparent;
  box-shadow: none;
}
```

Add the remaining existing TOC-page components with these mappings:

```css
[data-course-theme="fabmetric"][data-course-layout="toc"] :is(.step-badge, .subsection h3 .step-circle, .toc .step-num) {
  border: 1px solid #bfdbfe;
  border-radius: 6px;
  background: #eff6ff;
  color: var(--course-primary);
}

[data-course-theme="fabmetric"][data-course-layout="toc"] :is(.s3, .s6, .subsection.orange h3 .step-circle) {
  border-color: #ddd6fe;
  background: #f5f3ff;
  color: var(--course-tertiary);
}

[data-course-theme="fabmetric"][data-course-layout="toc"] :is(.s4, .s5, .step-new, .new-badge) {
  border-color: #fecaca;
  background: #fef2f2;
  color: var(--course-error);
}

[data-course-theme="fabmetric"][data-course-layout="toc"] .code-wrap {
  border: 1px solid #334155;
  border-radius: 8px;
  background: var(--course-code);
  box-shadow: none;
}

[data-course-theme="fabmetric"][data-course-layout="toc"] .code-header {
  border-color: #334155;
  background: var(--course-code-toolbar);
}

[data-course-theme="fabmetric"][data-course-layout="toc"] pre {
  background: var(--course-code);
  color: #e2e8f0;
  font-family: "JetBrains Mono", Consolas, monospace;
}

[data-course-theme="fabmetric"][data-course-layout="toc"] :is(.code-copy, .copy-btn) {
  min-height: 36px;
  border: 1px solid #475569;
  border-radius: 6px;
  background: #334155;
  color: #f8fafc;
}

[data-course-theme="fabmetric"][data-course-layout="toc"] .tbl-wrap {
  border: 1px solid var(--course-border);
  border-radius: 8px;
  background: var(--course-surface);
}

[data-course-theme="fabmetric"][data-course-layout="toc"] table th {
  background: var(--course-surface-low);
  color: var(--course-muted);
}

[data-course-theme="fabmetric"][data-course-layout="toc"] table td {
  border-color: #f1f5f9;
}

[data-course-theme="fabmetric"][data-course-layout="toc"] .callout {
  border: 1px solid var(--course-border);
  border-left-width: 3px;
  border-radius: 8px;
  background: var(--course-surface-low);
}

[data-course-theme="fabmetric"][data-course-layout="toc"] .callout-tip {
  border-left-color: var(--course-success);
  background: #ecfdf5;
}

[data-course-theme="fabmetric"][data-course-layout="toc"] .callout-info {
  border-left-color: var(--course-primary);
  background: #eff6ff;
}

[data-course-theme="fabmetric"][data-course-layout="toc"] .callout-warn {
  border-left-color: var(--course-warning);
  background: #fffbeb;
}

[data-course-theme="fabmetric"][data-course-layout="toc"] .callout-danger {
  border-left-color: var(--course-error);
  background: #fef2f2;
}

[data-course-theme="fabmetric"][data-course-layout="toc"] :is(.card, .stat-card, .compare-side, .summary-card) {
  border: 1px solid var(--course-border);
  border-radius: 8px;
  background: var(--course-surface);
  box-shadow: var(--course-shadow);
}

[data-course-theme="fabmetric"][data-course-layout="toc"] :is(.flow-step, .badge, .tag) {
  border-radius: 6px;
}

[data-course-theme="fabmetric"][data-course-layout="toc"] :is(#insights, #summary, [id^="ai-"]) {
  border: 1px solid var(--course-border) !important;
  border-left: 3px solid var(--course-tertiary) !important;
  border-radius: 8px !important;
  background: var(--course-surface) !important;
  box-shadow: none !important;
}
```

- [ ] **Step 4: Run the TOC structural verification**

Run:

```powershell
npm run verify:course-design -- --scope=toc
```

Expected: PASS with `course design verification passed: toc`.

- [ ] **Step 5: Verify anchors, observer state, and copy behavior**

At 1440x900, open both TOC pages from the local server. On 05, click `#step3`; on 06, click `#step8`. Verify the URL fragment and viewport section change, the corresponding TOC item receives the existing active styling, and the first code copy button on each page enters its copied state with no console error.

- [ ] **Step 6: Commit the TOC adapter**

```powershell
git add Web/반도체_공정_데이터분석.html Web/실전_반도체_공정_데이터분석_강의자료.html Web/assets/course-design-system.css
git commit -m "반도체 강좌에 공통 디자인 적용"
```

### Task 4: Responsive, Accessibility, Print, and End-to-End Verification

**Files:**
- Modify: `Web/assets/course-design-system.css`
- Modify: `Web/index.html` through `npm run build`

**Interfaces:**
- Consumes: all three integrated pages from Tasks 2 and 3.
- Produces: the final responsive and accessible stylesheet contract plus a regenerated static index.

- [ ] **Step 1: Run the complete contract before adding final media rules**

Run:

```powershell
npm run verify:course-design -- --scope=all
```

Expected: FAIL on the first missing item among `:focus-visible`, `@media (max-width: 767px)`, reduced motion, print, or horizontal overflow.

- [ ] **Step 2: Add focus, overflow, mobile, reduced-motion, and print rules**

Append these rules and keep all selectors theme-scoped:

```css
[data-course-theme="fabmetric"] :is(a, button):focus-visible {
  outline: 3px solid rgba(37, 99, 235, 0.3);
  outline-offset: 3px;
}

[data-course-theme="fabmetric"] :is(.tbl-wrap, .table-wrap, .code-wrap, pre) {
  max-width: 100%;
  overflow-x: auto;
}

@media (max-width: 767px) {
  [data-course-theme="fabmetric"] :is(.site-header, header) {
    padding: 32px 16px 28px;
  }

  [data-course-theme="fabmetric"] :is(.site-header h1, header h1) {
    font-size: 28px;
    line-height: 1.28;
  }

  [data-course-theme="fabmetric"][data-course-layout="tabs"] .main,
  [data-course-theme="fabmetric"][data-course-layout="toc"] .layout {
    width: 100%;
    padding: 24px 16px;
  }

  [data-course-theme="fabmetric"][data-course-layout="toc"] .layout {
    flex-direction: column;
  }

  [data-course-theme="fabmetric"][data-course-layout="toc"] .toc {
    position: static;
    width: 100%;
  }

  [data-course-theme="fabmetric"] :is(.section, .session-header, .content-card) {
    padding: 16px;
  }

  [data-course-theme="fabmetric"] :is(.nav-tab, button, .code-copy, .copy-btn) {
    min-height: 40px;
  }
}

@media (prefers-reduced-motion: reduce) {
  [data-course-theme="fabmetric"] *,
  [data-course-theme="fabmetric"] *::before,
  [data-course-theme="fabmetric"] *::after {
    scroll-behavior: auto !important;
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }
}

@media print {
  [data-course-theme="fabmetric"] :is(.nav-bar, .toc, .copy-btn, .code-copy) {
    display: none !important;
  }

  [data-course-theme="fabmetric"],
  [data-course-theme="fabmetric"] :is(.section, .content-card, .session-header) {
    color: #000 !important;
    background: #fff !important;
    box-shadow: none !important;
  }
}
```

- [ ] **Step 3: Run all structural checks**

Run:

```powershell
npm run verify:course-design -- --scope=all
```

Expected: PASS with `course design verification passed: all`.

- [ ] **Step 4: Build the static index**

Run:

```powershell
npm run build
```

Expected: exit code 0, no missing entry warning, and a regenerated `Web/index.html` containing the same ordered course links.

- [ ] **Step 5: Run desktop visual verification**

At 1440x900, capture the first viewport of all three pages and verify:

- solid cool-white canvas with blue technical accents;
- no decorative radial orb or multicolor hero gradient;
- 01 uses a stable three-tab row;
- 05 and 06 use a 240px TOC beside the content;
- headings, cards, labels, and buttons do not overlap;
- 06 retains red defect and violet ML emphasis without becoming a one-color theme.

- [ ] **Step 6: Run mobile visual verification**

At 390x844, capture the top and one content section of all three pages. In the browser evaluate:

```js
({
  viewport: document.documentElement.clientWidth,
  scrollWidth: document.documentElement.scrollWidth,
  overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
})
```

Expected on every page: `overflow` is `false`. Verify long tables and code blocks scroll inside their own containers, titles fit, controls remain at least 40px high, and the TOC sits above the body.

- [ ] **Step 7: Check browser errors and missing local assets**

Inspect console logs and network-visible page state for all three pages. Expected: no JavaScript error, no missing `course-design-system.css`, and no missing course-local CSV or image caused by the theme integration. Ignore the browser's optional `favicon.ico` request if it is the only 404.

- [ ] **Step 8: Check print rendering**

Open print preview for one tabs page and one TOC page. Expected: navigation and copy controls are hidden, text remains black on white, and code content is present without clipping the page horizontally.

- [ ] **Step 9: Review the final diff and encoding**

Run:

```powershell
git diff --check
git diff --stat
git status --short
```

Expected: no whitespace error; only the planned CSS, verifier, package metadata, three course HTML files, generated `Web/index.html` when changed, and this plan are modified. `stitch-reference/` remains untracked and untouched.

- [ ] **Step 10: Commit final responsive rules and generated index**

```powershell
git add Web/assets/course-design-system.css Web/index.html
git commit -m "강좌 디자인 반응형 검증 완료"
```

If `npm run build` produces no `Web/index.html` diff, omit that file from `git add` and commit only the stylesheet.
