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


def picture(item, main=False):
    dimensions = f' width="{int(item["width"])}" height="{int(item["height"])}"'
    if item["width"] <= 0 or item["height"] <= 0:
        raise ValueError("Reviewed image dimensions are required: " + item["src"])
    loading = 'fetchpriority="high"' if main else 'loading="lazy"'
    image = f'<img src="{escape(item["src"])}" alt="{escape(item["alt"])}"{dimensions} {loading} decoding="async">'
    return f'<a class="zoom-image" href="{escape(item["src"])}" aria-label="画像を拡大：{escape(item["alt"])}">{image}</a>'


def figure(item, main=False):
    classes = ["main-figure"] if main else []
    classes.append(item["kind"])
    caption = "<br>".join(escape(line) for line in item["caption"].splitlines())
    if item.get("evaluation_symbol"):
        caption = '<span class="evaluation-symbol" aria-hidden="true">' + escape(item["evaluation_symbol"]) + "</span>" + caption
    if item["kind"] == "photograph-group":
        image = '<div class="paired-images">' + "".join(picture(image) for image in item["images"]) + "</div>"
    else:
        image = picture(item, main)
    photo_links = ""
    if item.get("photo_links"):
        photo_links = ('  <ul class="photo-links" aria-label="写真ごとの説明">' + "".join(
            f'<li><a href="{escape(link["src"])}">{escape(link["text"])}</a></li>'
            for link in item["photo_links"]) + '</ul>\n')
    caption_html = f'  <figcaption>{caption}</figcaption>\n' if caption else ""
    return (f'<figure class="{" ".join(classes)}">\n'
            f'  {image}\n' + photo_links + caption_html + '</figure>')


def column(item, index):
    heading_id = f'column-{index}'
    icon = item.get("icon", {"src": "/images/column-icon.png", "width": 106, "height": 102})
    icon_html = (f'<img class="column-icon" src="{escape(icon["src"])}" alt="" '
                 f'width="{int(icon["width"])}" height="{int(icon["height"])}" loading="lazy">') if icon else ""
    paragraphs = ""
    for text in item["paragraphs"]:
        rendered = escape(text)
        for marker in item.get("footnote_markers", []):
            rendered = rendered.replace(escape(marker), f'<sup>{escape(marker)}</sup>')
        paragraphs += f'\n  <p>{rendered}</p>'

    figures = "".join("\n" + figure(item) for item in item.get("figures", []))
    source = ('\n  <p class="column-source">' + "<br>".join(escape(line) for line in item["source"].splitlines()) + "</p>") if item.get("source") else ""
    if item["title"]:
        label = f'aria-labelledby="{heading_id}"'
        heading = f'<h2 id="{heading_id}">{icon_html}{escape(item["title"])}</h2>'
    else:
        label = 'aria-label="原著のコラム"'
        heading = f'<div class="column-heading">{icon_html}</div>'
    return (f'\n<section class="column" {label}>\n'
            f'  {heading}'
            + paragraphs + figures + source + '\n</section>')


def case_study(item):
    paragraphs = "".join(f'<p>{escape(text)}</p>' for text in item["paragraphs"])
    tone = item.get("tone", "yellow")
    if tone not in ("yellow", "blue"):
        raise ValueError("Unknown case study tone: " + tone)
    extra_class = " case-study--blue" if tone == "blue" else ""
    if "figures" in item:
        heading = f'<h2>{escape(item["title"])}</h2>' if item.get("title") else ""
        intro = "".join(f'<p>{escape(text)}</p>' for text in item.get("intro_paragraphs", []))
        figures = '<div class="figure-gallery">' + "".join(figure(image) for image in item["figures"]) + '</div>'
        return (f'\n<aside class="case-study{extra_class} case-study--multiple" aria-label="掲載事例">'
                + heading + intro + '<div class="case-study-content"><div>' + paragraphs
                + '</div>' + figures + '</div></aside>')
    if item.get("text_after"):
        return (f'\n<aside class="case-study{extra_class} case-study--stacked" aria-label="掲載事例">'
                + figure(item["figure"]) + '<div>' + paragraphs + '</div></aside>')
    return (f'\n<aside class="case-study{extra_class}" aria-label="掲載事例"><div>' + paragraphs
            + '</div>' + figure(item["figure"]) + '</aside>')


def render_figures(data):
    figures = data["figures"]
    if "figure_sections" in data:
        sections = data["figure_sections"]
        if [index for section in sections for index in section["indices"]] != list(range(len(figures))):
            raise ValueError("figure_sections must preserve the original figure order")
        rendered = []
        for index, section in enumerate(sections, start=1):
            count = section.get("columns", 2)
            if count not in (2, 3):
                raise ValueError("Figure sections support two or three columns")
            tone = " figure-section--blue" if section.get("tone") == "blue" else ""
            title = section.get("title", "")
            heading = f'<h2 id="figure-section-{index}">{escape(title)}</h2>' if title else ""
            label = f' aria-labelledby="figure-section-{index}"' if title else ' aria-label="掲載図版"'
            rendered.append(f'<section class="figure-section{tone}"{label}>' + heading
                            + f'<div class="figure-gallery figure-gallery--{count}">'
                            + ''.join(figure(figures[i]) for i in section["indices"]) + '</div></section>')
        return ''.join(rendered)
    if "figure_rows" in data:
        rows = data["figure_rows"]
        if [index for row in rows for index in row] != list(range(len(figures))):
            raise ValueError("figure_rows must preserve the original figure order")
        layout = data.get("first_row_layout", "equal")
        if layout not in ("equal", "three-one"):
            raise ValueError("Unknown first figure row layout: " + layout)
        alignment = data.get("first_row_align", "start")
        if alignment not in ("start", "end"):
            raise ValueError("Unknown first figure row alignment: " + alignment)
        return '<div class="figure-rows">' + ''.join(
            '<div class="figure-gallery' + (' figure-row--three-one' if i == 0 and layout == 'three-one' else '')
            + (' figure-row--end' if i == 0 and alignment == 'end' else '') + '">'
            + ''.join(figure(figures[index]) for index in row) + '</div>'
            for i, row in enumerate(rows)) + '</div>'
    if "figure_columns" in data:
        groups = data["figure_columns"]
        if sorted(index for group in groups for index in group) != list(range(len(figures))):
            raise ValueError("Every figure must occur once in figure_columns")
        return '<div class="figure-gallery">' + ''.join(
            '<div class="figure-column">' + ''.join(figure(figures[index]) for index in group) + '</div>'
            for group in groups) + '</div>'
    rendered = figure(figures[0], main=True) if figures else ""
    if len(figures) > 1:
        layout = data.get("secondary_layout", "equal")
        if layout not in ("equal", "one-two", "single"):
            raise ValueError("Unknown secondary figure layout: " + layout)
        extra_class = " figure-pair--" + layout if layout != "equal" else ""
        rendered += f'\n<div class="figure-pair{extra_class}">\n' + "\n".join(figure(item) for item in figures[1:]) + "\n</div>"
    return rendered


def build(path, output=None):
    data = json.loads(path.read_text(encoding="utf-8"))
    if output is None:
        output = ROOT / (data["slug"] + ".html")
    elif not output.is_absolute():
        output = ROOT / output
    is_preview = "preview" in output.relative_to(ROOT).parts
    related = []
    for item in data["related"]:
        text = escape(item["text"])
        related.append(f'<a href="{escape(item["href"])}">{text}</a>' if item.get("href") else text)
    rendered = render_figures(data)
    values = {key: escape(data[key]) for key in ("id", "title", "english", "category", "principle", "body", "note")}
    values["page_title"] = escape(data["id"] + " " + data["title"])
    values.update({"source_" + key: escape(value) for key, value in data["source"].items()})
    values.update(related="、".join(related), figures=rendered,
                  columns="".join(case_study(item) for item in data.get("case_studies", []))
                  + "".join(column(item, index) for index, item in enumerate(data.get("columns", []), start=1)))
    if data.get("body_paragraphs"):
        if "".join(data["body_paragraphs"]) != data["body"]:
            raise ValueError("body_paragraphs must preserve the complete original body")
        values["body"] = "<br>".join(escape(text) for text in data["body_paragraphs"])
    values["definition"] = '    <p class="definition">' + escape(data["note"]) + "</p>" if data["note"] else ""
    values["edition_note"] = ("Web版の図版は原図の構図に基づき清書・彩色しています。" if any(
        item["kind"] == "illustration" for item in data["figures"])
        else "写真は原著編集データからWeb表示用に変換しています。")
    values["robots_meta"] = '<meta name="robots" content="noindex, nofollow">' if is_preview else ""
    values["preview_notice"] = '<p class="preview-notice">制作確認用プレビュー</p>' if is_preview else ""
    if is_preview and data.get("review_url"):
        values["preview_notice"] = ('<p class="preview-notice">制作確認用プレビュー · '
                                    f'<a href="{escape(data["review_url"])}">原図との比較・照合記録</a></p>')
    page = Template((ROOT / "templates/keyword.html").read_text(encoding="utf-8")).substitute(values)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content", nargs="?", type=Path, default=ROOT / "content/keywords/a-4.json")
    parser.add_argument("--output", type=Path, help="Explicit output path (default: formal page)")
    args = parser.parse_args()
    build(args.content, args.output)
