#!/usr/bin/env python3
"""Convertit un PRIVACY.md (titres, paragraphes, **gras**, [liens](url)) en page HTML.

Usage : python3 tools/privacy_html.py <PRIVACY.md> <sortie.html>
"""
import html
import re
import sys


def inline(text: str) -> str:
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', t)
    return t


def convert(md: str) -> tuple[str, str]:
    title, parts, para = "Privacy policy", [], []

    def flush():
        if para:
            parts.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    for line in md.splitlines():
        s = line.strip()
        m = re.match(r"^(#{1,3})\s+(.*)$", s)
        if m:
            flush()
            level = len(m.group(1))
            if level == 1:
                title = m.group(2)
            lang = ' lang="fr"' if m.group(2).lower().startswith("fran") else ""
            parts.append(f"<h{level}{lang}>{inline(m.group(2))}</h{level}>")
        elif not s:
            flush()
        else:
            para.append(s)
    flush()
    return title, "\n".join(parts)


def main() -> None:
    src, out = sys.argv[1], sys.argv[2]
    title, body = convert(open(src, encoding="utf-8").read())
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>
  :root {{ color-scheme: light dark; --bg: #fffdf6; --fg: #2a2620; --muted: #6b645a; --link: #3150c9; }}
  @media (prefers-color-scheme: dark) {{ :root {{ --bg: #1d1b18; --fg: #ece6da; --muted: #a9a195; --link: #9fb3ff; }} }}
  body {{ background: var(--bg); color: var(--fg); font: 17px/1.6 system-ui, sans-serif; margin: 0; padding: 24px 16px 48px; }}
  main {{ max-width: 720px; margin: 0 auto; }}
  h1 {{ font-size: 1.6em; line-height: 1.25; }}
  h2 {{ margin-top: 2em; border-top: 1px solid color-mix(in srgb, var(--fg) 15%, transparent); padding-top: 1em; }}
  a {{ color: var(--link); }}
</style>
</head>
<body>
<main>
{body}
</main>
</body>
</html>
"""
    open(out, "w", encoding="utf-8").write(page)


if __name__ == "__main__":
    main()
