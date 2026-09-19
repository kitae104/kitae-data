---
name: FabMetric Telemetry
colors:
  surface: '#faf8ff'
  surface-dim: '#d2d9f4'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3ff'
  surface-container: '#eaedff'
  surface-container-high: '#e2e7ff'
  surface-container-highest: '#dae2fd'
  on-surface: '#131b2e'
  on-surface-variant: '#434655'
  inverse-surface: '#283044'
  inverse-on-surface: '#eef0ff'
  outline: '#737686'
  outline-variant: '#c3c6d7'
  surface-tint: '#0053db'
  primary: '#004ac6'
  on-primary: '#ffffff'
  primary-container: '#2563eb'
  on-primary-container: '#eeefff'
  inverse-primary: '#b4c5ff'
  secondary: '#00687a'
  on-secondary: '#ffffff'
  secondary-container: '#57dffe'
  on-secondary-container: '#006172'
  tertiary: '#6a1edb'
  on-tertiary: '#ffffff'
  tertiary-container: '#8343f4'
  on-tertiary-container: '#f7edff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#acedff'
  secondary-fixed-dim: '#4cd7f6'
  on-secondary-fixed: '#001f26'
  on-secondary-fixed-variant: '#004e5c'
  tertiary-fixed: '#eaddff'
  tertiary-fixed-dim: '#d2bbff'
  on-tertiary-fixed: '#25005a'
  on-tertiary-fixed-variant: '#5a00c6'
  background: '#faf8ff'
  on-background: '#131b2e'
  surface-variant: '#dae2fd'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.025em
  headline-xl-mobile:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.015em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  mono-data:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: -0.01em
  mono-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '400'
    lineHeight: 14px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.04em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-lg: 1.5rem
  margin: 1rem
  margin-md: 1.5rem
  margin-lg: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system targets semiconductor fab process engineers, yield analysis specialists, and data science researchers. It balances the uncompromising precision of industrial fabrication telemetry with the frictionless clarity of high-performance analytics dashboards.

The emotional core is **controlled precision, cleanroom clarity, and analytical confidence**. Interfaces must feel calibrated like an optical inspection bench: devoid of decorative noise, highly legible under continuous operational shifts, and instantly responsive.

### Visual Style
The design blends **Modern Technical / Instrumental Corporate** with **Micro-tactile Precision**:
- **Cleanroom Canvas:** Sterile, high-efficiency cool-slate neutrals frame intense data streams.
- **Instrument Signals:** Highly saturated spectral accents (Electric Blue, Wafer Cyan, and ML Violet) highlight telemetry anomalies, wafer binning categories, and model inferences against calm, calibrated backdrops.
- **Micro-linear Structure:** Precise 1px borders, subtle data grids, and hairline visual dividers evoke clean wafer layouts and analytical reticles.

## Colors

The color architecture enforces strict functional semantics to support split-second analytical reading across fabrication lines and training models:

- **Primary (`#2563EB` - Semiconductor Electric Blue):** Primary actions, active navigation states, wafer lot identifiers, and standard telemetry curves.
- **Secondary (`#06B6D4` - Telemetry Cyan):** In-situ sensor readings, active plasma state indicators, wafer map heatmaps, and running process loops.
- **Tertiary (`#7C3AED` - ML Deep Purple):** Model inference nodes, Orange3 pipeline tags, feature engineering badges, and automated anomaly classification.
- **Neutral / Structural (`#0F172A` - Cleanroom Deep Navy):** High-contrast typography, structural dark framing, and terminal chrome.

### Functional & Surface Roles
- **Canvas Base:** `#F8FAFC` (cool slate-tinted white preventing optic fatigue under cleanroom fluorescent illumination).
- **Card Surface:** `#FFFFFF` (isolated, pure white container planes).
- **Borders & Dividers:** `#E2E8F0` (refined, 1px crisp structural boundaries).
- **Muted Text / Metadata:** `#64748B` (secondary units, lot timestamps, process run IDs).
- **Semiconductor Process Status:**
  - **Nominal / Die Yield Pass:** `#10B981` (Success Green)
  - **Threshold Drift / Marginal Spec:** `#F59E0B` (Warning Amber)
  - **Excursion / Die Defect Reject:** `#EF4444` (Critical Red)

## Typography

Typography prioritizes tabular numerical stability, cross-lingual density (Hangul + Latin), and rapid scanning.

- **Primary Interface Font:** `Inter` (with native fallback to `Pretendard` or `Noto Sans KR` for full CJK glyph parity). High x-height, neutral geometric construction, and open counters guarantee legibility across multi-column data views.
- **Telemetry & Technical Monospace:** `JetBrains Mono` for wafer coordinates, chamber pressures, sensor streaming payloads, recipe scripts, and model hyperparameter tables.
- **Tabular Numerics:** All dynamic numerical indicators, yield percentages, and telemetry counters must activate `font-feature-settings: "tnum" 1, "cv05" 1` to prevent layout reflow during live data pushes.
- **Case Rules:** Operational status badges and sensor metric labels use uppercase letter spacing (`letterSpacing: 0.04em`) to distinctly decouple metadata tags from prose readouts.

## Layout & Spacing

The portal relies on a **dense fluid-modular grid** calibrated to display dense telemetry arrays, real-time charts, and interactive wafer maps simultaneously without unnecessary vertical scrolling.

### Grid & Canvas Structure
- **Desktop (>= 1280px):** 12-column layout with fixed 240px contextual tool drawer/navigation, `1.5rem` gutters, and `2rem` outer margins. Modules adhere to 3, 4, 6, 8, or 12 column cards.
- **Tablet (768px - 1279px):** 8-column layout with `1rem` gutters and `1.5rem` margins. Side drawers collapse into floating quick-switch panels.
- **Mobile (< 768px):** 4-column layout with `0.75rem` gutters and `1rem` outer margins. Multi-metric instrument clusters stack into single-column expandable accordion rows.

### Spacing Rhythms
- Use strict 4px base units (`0.25rem`). Component internals enforce compact density: `0.5rem` (8px) for compact toolbars, `1rem` (16px) for standard metric card interiors, and `1.5rem` (24px) for expansive analytical chart canvases.

## Elevation & Depth

Visual hierarchy is achieved through **refined surface elevation and crisp boundary delineation** rather than heavy blurred drops. The aesthetic echoes optical glass instrumentation.

### Elevation Levels
- **Level 0 (Canvas Base):** Flat `#F8FAFC`. Base grounding plane for tool views and page layouts.
- **Level 1 (Card & Module Surfaces):** Solid `#FFFFFF` enclosed with a crisp `1px solid #E2E8F0` border and an ambient structural drop shadow: `0 1px 3px 0 rgba(15, 23, 42, 0.05), 0 1px 2px -1px rgba(15, 23, 42, 0.03)`.
- **Level 2 (Interactive Floating Elements / Popovers):** Elevated contextual parameter controllers and telemetry tooltips use `#FFFFFF` with `0 4px 6px -1px rgba(15, 23, 42, 0.08), 0 2px 4px -2px rgba(15, 23, 42, 0.04)` combined with `1px solid #CBD5E1`.
- **Level 3 (Modal Dialogs & Wafer Defect Inspect Overlays):** `#FFFFFF` paired with an ambient backdrop overlay (`rgba(15, 23, 42, 0.4)` with `backdrop-filter: blur(4px)`) and a directional lift shadow: `0 20px 25px -5px rgba(15, 23, 42, 0.12), 0 8px 10px -6px rgba(15, 23, 42, 0.06)`.
- **Telemetry Glow (State Accents):** High-priority alerts and live active process chambers utilize a subtle inner/outer halo: `box-shadow: 0 0 0 1px #06B6D4, 0 0 12px -2px rgba(6, 182, 212, 0.35)`.

## Shapes

The design system employs a **controlled rounded curvature (Level 2)** calibrated between 10px and 16px to balance technical rigor with modern dashboard ergonomics.

- **Primary Cards & Containers:** `rounded-lg` (16px / `1rem`) creates distinct modular units on the canvas.
- **Buttons, Form Inputs, & Tab Selectors:** `rounded-md` (10px / `0.625rem`) provides a responsive touch/click target while maintaining structural linearity.
- **Badges, Chips, & Micro Data Tags:** `rounded-sm` (6px / `0.375rem`) ensures dense data grids and wafer map legend items remain compact without pill-shaped visual bulk.
- **Circular Elements:** Die selection indicators, lot progress rings, and sensor heartbeat dots retain exact 50% circular geometry (`rounded-full`).

## Components

### Buttons
- **Primary:** Background `#2563EB`, text `#FFFFFF`, border `transparent`, border-radius `10px`. Hover: `#1D4ED8`. Active: scale `0.99`. Subtle inset top highlight for tactile precision.
- **Secondary (Telemetry Tool):** Background `#FFFFFF`, border `1px solid #E2E8F0`, text `#0F172A`. Hover: `#F1F5F9`, border `#CBD5E1`.
- **Tertiary / ML Action:** Background `#F5F3FF`, border `1px solid #DDD6FE`, text `#7C3AED`. Hover: `#EDE9FE`.
- **Icon Utility:** 36x36px square with 10px corner radius, transparent background, text `#64748B`, hover text `#0F172A`.

### Chips & Badges
- **Status Chips:** Height 22px, padding `2px 8px`, border-radius `6px`, font `JetBrains Mono` 11px uppercase weight 600.
  - *Pass/Yield:* Text `#065F46`, background `#ECFDF5`, border `1px solid #A7F3D0`.
  - *Drift/Warning:* Text `#92400E`, background `#FFFBEB`, border `1px solid #FDE68A`.
  - *Defect/Fault:* Text `#991B1B`, background `#FEF2F2`, border `1px solid #FECACA`.
- **Machine Learning Tag:** Background `#FAF5FF`, text `#6D28D9`, border `1px solid #E9D5FF` with a small 6px solid `#7C3AED` leading dot.

### Inputs & Selectors
- **Input Fields:** Height 38px, background `#FFFFFF`, border `1px solid #E2E8F0`, radius `10px`, typography `Inter` 14px. Focus state: border `#2563EB`, box-shadow `0 0 0 3px rgba(37, 99, 235, 0.15)`.
- **Parameter Stepper / Range:** Crisp numeric readout set in `JetBrains Mono` accompanied by dual micro-stepper actions.

### Data Cards & Sensor Telemetry Panels
- **Telemetry Card:** Pure `#FFFFFF` surface, `1px solid #E2E8F0` border, `16px` corner radius, `1rem` interior padding. Header contains micro-kicker in secondary text (`#64748B`), large tabular numerical value (`24px`, `#0F172A`), sparkline or run-chart, and delta percentage indicator.
- **Wafer Map Canvas Frame:** Dark-mode or neutral-high contrast container inset with hairline grid coordinates, interactive canvas viewport, and zoom/pan mini-dock anchored to the bottom-right.

### Lists & Table Grids
- **Header:** Background `#F8FAFC`, bottom border `1px solid #E2E8F0`, font `Inter` 12px weight 600, text `#64748B`, uppercase tracking.
- **Row:** Height 44px, border-bottom `1px solid #F1F5F9`, hover background `#F8FAFC`. Monospaced tabular alignment for recipe IDs, chamber temps, and yield metrics.

### Checkboxes & Radio Controls
- **Checkbox:** 18x18px, radius `4px`, border `1.5px solid #CBD5E1`. Checked state: background `#2563EB`, border `#2563EB`, white micro-checkmark icon.
- **Radio:** 18x18px circular, checked state features a distinct 6px centered dot in `#2563EB`.