---
name: Clarify Mobile
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#444651'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#757682'
  outline-variant: '#c5c5d3'
  surface-tint: '#4059aa'
  primary: '#00236f'
  on-primary: '#ffffff'
  primary-container: '#1e3a8a'
  on-primary-container: '#90a8ff'
  inverse-primary: '#b6c4ff'
  secondary: '#006a61'
  on-secondary: '#ffffff'
  secondary-container: '#86f2e4'
  on-secondary-container: '#006f66'
  tertiary: '#272b2d'
  on-tertiary: '#ffffff'
  tertiary-container: '#3d4143'
  on-tertiary-container: '#aaadaf'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dce1ff'
  primary-fixed-dim: '#b6c4ff'
  on-primary-fixed: '#00164e'
  on-primary-fixed-variant: '#264191'
  secondary-fixed: '#89f5e7'
  secondary-fixed-dim: '#6bd8cb'
  on-secondary-fixed: '#00201d'
  on-secondary-fixed-variant: '#005049'
  tertiary-fixed: '#e0e3e5'
  tertiary-fixed-dim: '#c4c7c9'
  on-tertiary-fixed: '#191c1e'
  on-tertiary-fixed-variant: '#444749'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  headline-lg:
    fontFamily: Geist
    fontSize: 30px
    fontWeight: '700'
    lineHeight: 38px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Geist
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
  label-caps:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  mono-label:
    fontFamily: Geist
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  container-margin: 20px
  gutter: 16px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 24px
  section-gap: 32px
---

## Brand & Style

The design system is centered on the concepts of clarity, efficiency, and reliability. It targets professional and academic users who need to digest high-density information quickly. The visual language follows a **Corporate Modern** aesthetic, prioritizing legibility and functional minimalism to reduce cognitive load while a user interacts with complex documents.

The interface should feel airy and expansive, utilizing generous white space to separate summary modules from original text. The emotional response is one of calm confidence—transforming the "noise" of a long PDF into "signal" through structured, systematic UI patterns.

## Colors

The palette is anchored by **Trust Blue** (#1E3A8A), a deep, authoritative navy used for primary actions, navigation headers, and key brand moments. **Accent Teal** (#0D9488) is used sparingly for highlights, success states, and interactive elements that require subtle distinction from the primary brand color.

Surface colors rely on a hierarchy of "Slate" grays. The background is pure white (#FFFFFF) for document reading, while application backgrounds use a very soft gray (#F8FAFC) to create a subtle distinction between the container and the content cards. Text contrast is strictly maintained using Slate 900 (#0F172A) for headings to ensure maximum readability against white backgrounds.

## Typography

This design system utilizes a dual-font approach to balance technical precision with reading comfort. **Geist** is used for all UI "chrome"—headlines, buttons, and labels—to provide a clean, slightly technical aesthetic that feels precise and modern. **Inter** is reserved for body text and long-form summaries, chosen for its exceptional legibility at small sizes and high x-height, which reduces eye strain during long reading sessions.

Headlines use tight letter spacing to feel "locked-in" and professional. Body text uses a generous line-height (1.6x) to ensure summaries are easily scannable.

## Layout & Spacing

The design system employs a **fluid grid** model tailored for mobile devices. It utilizes a 4-column system for narrow viewports (phones) and an 8-column system for tablets.

- **Safe Zones:** A standard 20px margin is maintained on the left and right edges of the screen to prevent content from feeling cramped.
- **Rhythm:** Vertical spacing follows an 8px incremental scale. Elements within a card (like a title and its summary) use `stack-sm` (8px), while distinct cards in a list use `stack-md` (16px).
- **Alignment:** All text-based content should align to the left to facilitate natural reading patterns, with the exception of primary action buttons which may be centered or full-width.

## Elevation & Depth

Hierarchy is established through **Tonal Layering** supplemented by **Ambient Shadows**. This design system avoids heavy drop shadows in favor of subtle, diffused shadows that lift cards off the soft-gray background.

- **Level 0 (Floor):** The base application background (#F8FAFC).
- **Level 1 (Cards):** White surfaces (#FFFFFF) with a 4% opacity black shadow, 8px blur, and 4px vertical offset. Used for summary snippets and file lists.
- **Level 2 (Modals/Active):** White surfaces with an 8% opacity black shadow, 16px blur, and 8px vertical offset. Used for floating action buttons or bottom sheets.
- **Dividers:** Used sparingly. When necessary, use a 1px border of Slate 100 (#F1F5F9) instead of a shadow to separate internal card sections.

## Shapes

The shape language is consistently **Rounded**, conveying a friendly yet professional SaaS character. 

- **Standard Elements:** Buttons, input fields, and small cards use a 0.5rem (8px) radius.
- **Large Containers:** Content cards and bottom sheets use the `rounded-lg` (16px) setting to create a distinct, nested appearance.
- **Interactive Indicators:** Elements like notification badges or active status dots use a full "Pill" radius.
- **Focus States:** Use a 2px solid stroke of Trust Blue with a 4px offset to ensure accessibility.

## Components

### Buttons
- **Primary:** Solid Trust Blue background with white Geist Medium text. 16px corner radius (rounded-lg) for a modern feel.
- **Secondary:** Ghost style with a 1px Slate 200 border and Trust Blue text.
- **Floating Action (FAB):** Circular button with Primary color and a white "plus" or "upload" icon, using Level 2 elevation.

### Cards
- Summary cards should feature a `label-caps` category tag (e.g., "EXECUTIVE SUMMARY") at the top, followed by a `headline-md` title. 
- Padding inside cards should be a consistent 16px or 20px.

### Input Fields
- Search and file name inputs use a soft gray background (#F1F5F9) with no border in their default state. Upon focus, they transition to a white background with a 1px Trust Blue border.

### Chips & Progress
- **Progress Bars:** Use a thin (4px) height. The track is Slate 100, and the filler is Accent Teal to indicate active summarization.
- **File Type Chips:** Small, light-blue background (#E0E7FF) with Trust Blue Geist Mono text (e.g., "PDF", "DOCX").

### Lists
- File lists should use chevron-right icons (Slate 400) to indicate drill-down capability. Each row should have a minimum height of 64px for easy tap targets.