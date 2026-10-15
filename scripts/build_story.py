#!/usr/bin/env python3
"""Build story pages from reviewed text and Web image metadata."""
import argparse
import html
import json
import re
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]


def escape(value):
    return html.escape(str(value), quote=True)


def linked_text(text, links):
    targets = {item["text"]: item["href"] for item in links}
    if not targets:
        return escape(text)
    pattern = re.compile("|".join(re.escape(key) for key in sorted(targets, key=len, reverse=True)))
    rendered, start = [], 0
    for match in pattern.finditer(text):
        rendered.append(escape(text[start:match.start()]))
        rendered.append(f'<a href="{escape(targets[match.group()])}">{escape(match.group())}</a>')
        start = match.end()
    rendered.append(escape(text[start:]))
    return "".join(rendered)


def marker(item):
    color = item["color"]
    if color not in ("red", "orange", "blue"):
        raise ValueError("Unknown original keyword marker color")
    return f'<span class="keyword-marker keyword-marker--{color}" aria-hidden="true">◆</span>'


def keyword_link(item):
    return (f'<a href="{escape(item["href"])}">' + marker(item)
            + escape(item["id"] + " " + item["text"]) + '</a>')


def figure(item, index):
    if not item["src"].startswith("/images/") or min(item["width"], item["height"]) <= 0:
        raise ValueError("Reviewed Web image and dimensions are required")
    loading = 'fetchpriority="high"' if index == 1 else 'loading="lazy"'
    image = (f'<a class="zoom-image" href="{escape(item["src"])}" aria-label="画像を拡大：{escape(item["alt"])}">'
             f'<img src="{escape(item["src"])}" alt="{escape(item["alt"])}" '
             f'width="{item["width"]}" height="{item["height"]}" {loading} decoding="async"></a>')
    regions = []
    for region in item["keyword_regions"]:
        x, y, width, height = region["rect"]
        if not (0 <= x < 1 and 0 <= y < 1 and 0 < width <= 1 - x and 0 < height <= 1 - y):
            raise ValueError("Keyword link must be within its diagram")
        style = f'left:{x * 100:.5f}%;top:{y * 100:.5f}%;width:{width * 100:.5f}%;height:{height * 100:.5f}%'
        regions.append(f'<a class="diagram-keyword" href="{escape(region["href"])}" '
                       f'style="{style}" title="{escape(region["text"])}" '
                       f'aria-label="{escape(region["text"])}"><span class="sr-only">{escape(region["text"])}</span></a>')
    overlay = '<div class="diagram-labels">' + "".join(regions) + '</div>'
    notes = "".join('<li>' + keyword_link(note)
                    + "".join('<p>' + escape(text) + '</p>' for text in note["paragraphs"]) + '</li>'
                    for note in item["notes"])
    labels = ('<p class="story-labels">' + "".join('<span>' + escape(text) + '</span>' for text in item["labels"]) + '</p>') if item["labels"] else ""
    caption = '<figcaption>' + escape(item["caption"]) + '</figcaption>' if item["caption"] else ""
    return ('<figure class="story-figure">\n<div class="story-diagram">' + image + overlay + '</div>'
            + caption + '<details class="story-notes"><summary>図中の説明・キーワード</summary><ul>'
            + notes + '</ul>' + labels + '</details>\n</figure>')


def build(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    for link in data["body_links"]:
        if not any(link["text"] in text for text in data["paragraphs"]):
            raise ValueError("Linked wording must appear in the original body")
    values = {key: escape(data[key]) for key in ("marker", "english")}
    values["page_title"] = escape("ストーリー" + data["marker"] + " " + data["title"])
    values["paragraphs"] = "".join('<p>' + linked_text(text, data["body_links"]) + '</p>' for text in data["paragraphs"])
    inline = data["number"] in (1, 4)
    items = ["<li>" + keyword_link(item) + ("、" if inline and index < len(data["keywords"]) - 1 else "") + "</li>"
             for index, item in enumerate(data["keywords"])]
    values["keywords"] = '<ul' + (' class="story-keywords--inline"' if inline else '') + '>' + "".join(items) + '</ul>'
    values["figures"] = "\n".join(figure(item, index) for index, item in enumerate(data["figures"], start=1))
    values.update({"source_" + key: escape(value) for key, value in data["source"].items()})
    output = ROOT / (data["slug"] + ".html")
    page = Template((ROOT / "templates/story.html").read_text(encoding="utf-8")).substitute(values)
    output.write_text("\n".join(line.rstrip() for line in page.split("\n")), encoding="utf-8")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content", nargs="*", type=Path, help="Reviewed story JSON; defaults to all stories")
    args = parser.parse_args()
    for path in args.content or sorted((ROOT / "content/stories").glob("*.json")):
        build(path)
