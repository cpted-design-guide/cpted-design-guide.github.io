# cpted-design-guide.github.io
Crime Prevention Urban Design Guide

制作とプレビュー確認・正式反映の手順は [preview/README.md](preview/README.md) を参照してください。

Web用画像は原則として `images/` 以下に保存し、`a-4-footpaths.png` や `c-1-windows.jpg` のようにキーワードIDと内容を示す名前を付けます。移動・改名時は、HTMLだけでなく `content/keywords/` の生成データとプレビュー・比較ページの参照も更新します。

原著のIllustrator・InDesign・TIFFなどの編集元データは公開リポジトリに保存せず、公開する画像はWeb表示用に変換したものだけにします。

キーワード編の全38項目を正式公開しています。今後の修正でも原著の本文・図版・元写真・キャプション・コラムを照合し、これまでの品質と共通デザインを維持します。コラムは共通の電球アイコンを用い、アイコンがある場合は見出しに「コラム」を重複表示しません。不明点・原著との相違は推測で補わず報告します。

各組の対象URL・原著との照合結果・未解決事項は [PRODUCTION.md](PRODUCTION.md) に記録します。

本文・キャプション・図版などに含まれる原著のページ番号による他ページへの誘導表記（「→p.8参照」など）は、Web版には再現しません。一方、他のキーワードを示す参照（A-5の図中の「A-4参照」など）は、原著どおり残します。出典を示す掲載ページ番号や原典PDFへのリンクとも区別します。

ストーリー①〜⑤（原著pp.70〜74）は `content/stories/` の照合済みJSON、`templates/story.html`、`scripts/build_story.py` で管理します。全5ページの再生成は `python3 scripts/build_story.py`、1ページだけなら `python3 scripts/build_story.py content/stories/story-1.json` を実行します。Python標準ライブラリだけで生成できます。

ストーリーのページも `assets/css/keyword.css` を利用し、大きな図版と図中リンクに必要なスタイルだけを `assets/css/story.css` に追加しています。図版は `images/story-*.webp` の可逆圧縮画像です。図中のリンク範囲は各JSONの `keyword_regions` に画像全体に対する比率で保存しています。図の構図を変えずに解像度だけを変更する場合も、画像の実寸に合わせて `width`・`height` を更新してください。本文のリンクは原文中の文字列をそのまま指定し、図の説明欄も原著の文言を使用します。
