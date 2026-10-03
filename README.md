# gabrielvalle-491.github.io

Personal portfolio of **Gabriel Valle** — Data & AI automation (Excel / PDF), Virtual Assistant, QA.
Published with GitHub Pages at <https://gabrielvalle-491.github.io/>.

- Static HTML + CSS + vanilla JavaScript. No build step, no dependencies.
- Bilingual: Spanish (default) and English, with a toggle that is remembered in `localStorage`.
- Light / dark theme follows the system setting (`prefers-color-scheme`).
- Printable CV at [`/cv/`](https://gabrielvalle-491.github.io/cv/) (use *Imprimir / Guardar PDF* to export a PDF).

## Structure

```
index.html            # home: hero, services, projects, skills, experience, contact
cv/index.html         # printable CV (print CSS included in the page)
assets/css/style.css  # shared styles and color tokens (light + dark)
assets/js/main.js     # language toggle (ES / EN)
scripts/check_site.py # quick HTML / link checker
.nojekyll             # serve files as-is on GitHub Pages
```

## How to edit

**Text in two languages.** Every visible text exists twice, marked with `data-l`:

```html
<span data-l="es">Ver proyectos</span><span data-l="en">View projects</span>
<p data-l="es">Texto en español…</p>
<p data-l="en">English text…</p>
```

CSS shows only the language set in `<html lang>`. When you change a text, change both versions.
Attributes are translated with `data-es-<attr>` / `data-en-<attr>` (supported: `content`, `aria-label`,
`title`), and the page title with `data-es-title` / `data-en-title` on `<html>`.

**Add a project.** In `index.html`, copy one `<article class="card project">` block inside
`#proyectos` and edit the title, problem, description, stack tags (`<ul class="tags">`) and links.
Add a `Demo` button only if there is a live demo. Remove the `<span class="status">` badge when a
project is finished. Also add a line to the *Proyectos* list in `cv/index.html`.

**Experience / skills.** Edit the `<ol class="timeline">` in `index.html` and the matching
`.job` blocks in `cv/index.html` (newest first).

**Colors.** Change the tokens at the top of `assets/css/style.css` (`--accent`, etc.); the dark
theme values are in the `@media (prefers-color-scheme: dark)` block right below.

## Check before publishing

```bash
python3 scripts/check_site.py             # tag balance, duplicate ids, internal links and #anchors
python3 scripts/check_site.py --external  # also request every external link
python3 -m http.server 8000               # preview at http://localhost:8000
```

## Publish

Repository **Settings → Pages → Build and deployment**: *Deploy from a branch*, branch `main`, folder `/ (root)`.
