# AGENTS.md

## Project Overview

- This repository contains Korean data-analysis teaching materials.
- Main content lives in Korean-named folders such as `기초/`, `판다스기초/`, `반도체/`, `데이터분석/`, and `Web/`.
- `Web/` is the static site served by Vercel. `scripts/generate-index.js` rebuilds `Web/index.html` from the HTML files in `Web/`.
- The repository includes Jupyter notebooks, CSV sample data, generated or hand-authored HTML lesson pages, and a small Node.js build script.

## Working Conventions

- Preserve Korean filenames, headings, examples, and instructional tone unless the user explicitly asks to rewrite them.
- Keep edits focused on the requested lesson, dataset, notebook, or web page. Do not reorganize course material broadly without asking.
- Treat CSV files as teaching assets. Do not normalize, rename, or regenerate them unless the task specifically requires it.
- When changing notebooks, prefer structured notebook-aware tooling when practical and keep the notebook valid JSON.
- When changing generated `Web/index.html`, update `Web/order.txt` or `scripts/generate-index.js` if the ordering or generation behavior should persist.
- Use UTF-8 for all text files.

## Commands

- Build the static web index: `npm run build`
- Local Python environment setup from the README:
  - `python -m venv .venv`
  - `.\\.venv\\Scripts\\activate.bat`
- Vercel deployment notes from the README:
  - `npm i -g vercel`
  - `vercel login`
  - `vercel --prod`

## Verification

- Run `npm run build` after changing files in `Web/`, `Web/order.txt`, or `scripts/generate-index.js`.
- If modifying a notebook, open or execute the relevant cells when feasible, or at least validate that the `.ipynb` remains parseable.
- There is no dedicated test suite configured in `package.json`; document any manual checks performed.

## Code Review Rules

- Flag changes that break `npm run build` or make `Web/index.html` inconsistent with `Web/order.txt`.
- Flag accidental corruption of Korean text encoding in notebooks, CSVs, and HTML pages.
- Flag broad rewrites of lesson content when the request only asked for a narrow correction.
