"""Quick static checks for the site (no dependencies).

- every HTML file parses with balanced tags
- ids are unique per page
- internal links point to existing files and existing #anchors
- with --external, external http(s) links are requested and must not fail

Usage:  python scripts/check_site.py [--external]
"""
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.ids, self.links, self.errors = [], [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        # <link> tags other than stylesheets (canonical, icon) are not navigation links
        if tag == "link" and a.get("rel") != "stylesheet":
            return self._open(tag)
        for key in ("href", "src"):
            if a.get(key):
                self.links.append(a[key])
        self._open(tag)

    def _open(self, tag):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1][0] != tag:
            self.errors.append(f"line {self.getpos()[0]}: unexpected </{tag}> (open: {self.stack[-1] if self.stack else None})")
            return
        self.stack.pop()


def parse(path):
    p = Page()
    p.feed(path.read_text(encoding="utf-8"))
    p.close()
    if p.stack:
        p.errors.append(f"unclosed tags: {p.stack}")
    return p


def main():
    external = "--external" in sys.argv
    pages = {f: parse(f) for f in ROOT.rglob("*.html") if ".git" not in f.parts}
    problems, ext_links = [], set()

    for f, p in pages.items():
        rel = f.relative_to(ROOT)
        problems += [f"{rel}: {e}" for e in p.errors]
        dupes = {i for i in p.ids if p.ids.count(i) > 1}
        if dupes:
            problems.append(f"{rel}: duplicate ids {sorted(dupes)}")
        for link in p.links:
            if link.startswith(("http://", "https://")):
                ext_links.add(link)
                continue
            if link.startswith(("mailto:", "data:", "javascript:")):
                continue
            target, _, anchor = link.partition("#")
            dest = (f.parent / target).resolve() if target else f
            if dest.is_dir():
                dest = dest / "index.html"
            if not dest.exists():
                problems.append(f"{rel}: broken link {link}")
            elif anchor and anchor not in pages.get(dest, parse(dest)).ids:
                problems.append(f"{rel}: missing anchor {link}")

    if external:
        for url in sorted(ext_links):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "site-check"})
                code = urllib.request.urlopen(req, timeout=15).status
            except Exception as e:  # noqa: BLE001
                code = e
            print(f"  {code}  {url}")
            if code != 200:
                problems.append(f"external link failed: {url} ({code})")

    print(f"Checked {len(pages)} pages, {len(ext_links)} external links")
    for pr in problems:
        print("ERROR", pr)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
