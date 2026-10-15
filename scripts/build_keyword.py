#!/usr/bin/env python3
"""Build a keyword page from reviewed content; runs with the Python standard library."""
import argparse
import html
import json
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]


def escape(value):
    return html.escape(str(value), quote=True)


def figure(item, main=False):
    classes = ["main-figure"] if main else []
    classes.append(item["kind"])
    caption = "<br>".join(escape(line) for line in item["caption"].splitlines())
    if item.get("evaluation_symbol"):
        caption = '<span class="evaluation-symbol" aria-hidden="true">' + escape(item["evaluation_symbol"]) + "</span>" + caption
    dimensions = f' width="{int(item["width"])}" height="{int(item["height"])}"'
    if item["width"] <= 0 or item["height"] <= 0:
        raise ValueError("Reviewed image dimensions are required: " + item["src"])
    loading = 'fetchpriority="high"' if main else 'loading="lazy"'
    image = f'<img src="{escape(item["src"])}" alt="{escape(item["alt"])}"{dimensions} {loading} decoding="async">'
    image = f'<a class="zoom-image" href="{escape(item["src"])}" aria-label="画像を拡大：{escape(item["alt"])}">{image}</a>'
    if item.get("image_crop_height"):
        crop_height = int(item["image_crop_height"])
        if not 0 < crop_height <= item["height"]:
            raise ValueError("Crop height must stay inside the image")
        # Keep the original asset intact; render its caption as readable HTML.
        image = f'<div class="figure-image" style="aspect-ratio:{int(item["width"])}/{crop_height}">{image}</div>'
    return (f'<figure class="{" ".join(classes)}">\n'
            f'  {image}\n'
            f'  <figcaption>{caption}</figcaption>\n</figure>')


def build(path, output=None):
    data = json.loads(path.read_text(encoding="utf-8"))
    if output is None:
        output = ROOT / "preview" / (data["slug"] + ".html")
    elif not output.is_absolute():
        output = ROOT / output
    is_preview = "preview" in output.relative_to(ROOT).parts
    related = []
    for item in data["related"]:
        text = escape(item["text"])
        related.append(f'<a href="{escape(item["href"])}">{text}</a>' if item.get("href") else text)
    figures = data["figures"]
    rendered = figure(figures[0], main=True)
    if len(figures) > 1:
        rendered += '\n<div class="figure-pair">\n' + "\n".join(figure(item) for item in figures[1:]) + "\n</div>"
    values = {key: escape(data[key]) for key in ("id", "title", "english", "category", "principle", "body", "note")}
    values["page_title"] = escape(data["id"] + " " + data["title"])
    values.update({"source_" + key: escape(value) for key, value in data["source"].items()})
    values.update(related="、".join(related), figures=rendered)
    values["robots_meta"] = '<meta name="robots" content="noindex, nofollow">' if is_preview else ""
    values["preview_notice"] = '<p class="preview-notice">制作確認用プレビュー</p>' if is_preview else ""
    page = Template((ROOT / "templates/keyword.html").read_text(encoding="utf-8")).substitute(values)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content", nargs="?", type=Path, default=ROOT / "content/keywords/a-4.json")
    parser.add_argument("--output", type=Path, help="Explicit output path; formal pages require separate approval")
    args = parser.parse_args()
    build(args.content, args.output)
