# キーワードページのプレビュー運用

新しいページと修正案は、まず `preview/<既存のページ名>.html` に公開して確認する。承認を得るまでは、正式ページの上書き、トップからのリンク追加、正式ページへの反映を行わない。

A-4の確認用URL：

https://cpted-design-guide.github.io/preview/a-4-permeability.html

B-7・D-2の確認用URL：

- https://cpted-design-guide.github.io/preview/b-7-visibility-in-parks.html
- https://cpted-design-guide.github.io/preview/d-2-maintenance-participation.html

A-1・C-1の改修案（正式反映前）：

- https://cpted-design-guide.github.io/preview/a-1-walkability.html
- https://cpted-design-guide.github.io/preview/c-1-windows-facing-public-spaces.html
- https://cpted-design-guide.github.io/preview/a-1-c-1-source-review.html （原図との比較・照合記録）

## 再生成

リポジトリ直下で実行する。Python標準ライブラリだけで動作する。

```sh
python3 scripts/build_keyword.py content/keywords/a-4.json
python3 scripts/build_keyword.py content/keywords/b-7.json
python3 scripts/build_keyword.py content/keywords/d-2.json
python3 scripts/build_keyword.py content/keywords/a-1.json
python3 scripts/build_keyword.py content/keywords/c-1.json
```

既定の出力先は `preview/`。本文・掲載順・キャプションは原本と照合した `content/keywords/` のデータを利用し、`templates/keyword.html` と `assets/css/keyword.css` で表示する。

プレビューページには識別表示と `noindex, nofollow` を付ける。ただし、GitHub Pagesとこのリポジトリの内容は公開情報であり、アクセス制限ではない。

## 確認と正式反映

1. 原著PDF・編集データで本文、図版、写真、キャプション、掲載順、コラムの有無を照合する。
2. 図は原図と清書・彩色版を比較し、住宅・道路・人物・視線・動線・矢印・文字を確認する。
3. 公開したプレビューで、画像、PC・スマートフォン表示、リンクを確認する。
4. 利用者の承認後にだけ正式ページを生成・反映し、トップや関連キーワードのリンクを更新する。

画像のHTML寸法はファイルの実寸と一致させる。画像内キャプションをHTMLへ移す場合は、図の領域を保ったWeb用画像を作り、CSSによる隠れた切り抜きに依存しない。原本は公開リポジトリ外に保全し、原文・写真・図版の掲載要素を省略しない。

承認後のA-4正式ページの再生成：

```sh
python3 scripts/build_keyword.py content/keywords/a-4.json --output a-4-permeability.html
```

`--output` は出力先を明示するためのオプション。正式ページへの出力は別途承認が必要。

公開リポジトリにはWeb表示用に変換した画像だけを追加する。AI、InDesign、TIFF、編集用PDFなどの原著編集データや認証情報は追加しない。

## B-7・D-2の原著照合記録

| 項目 | B-7 見通しの良い公園 | D-2 維持管理活動への参加 |
|---|---|---|
| 原著の掲載箇所 | p.44（キーワード編PDF内30ページ目） | p.61（同47ページ目） |
| 本文・関連キーワード | 公開PDFと照合し全文掲載 | 公開PDFと照合し全文掲載。「B-1 コラム参照」も保持 |
| 図版 | 1点。`p44-zu.ai` の図と誌面を照合して清書・彩色 | 1点。`p61-zu.tif` の図と誌面を照合して清書・彩色 |
| 写真 | 2点。`p44-photo1.ai` 内の元写真と `p44-photo2.tif` | 3点。`p61-photo1.tif`〜`p61-photo3.tif` |
| キャプション | 図1件・写真2件を原著どおり掲載 | 図1件・写真2件を原著どおり掲載。清掃写真とサイン写真の2点には共通のキャプション |
| 独立したコラム | なし | なし |

ファイル名だけで対応を決めず、写真の被写体・誌面上の位置と、図の人物・行動・矢印・樹木・道具を比較した。D-2の写真は左から「道路沿いの花育て」「公園清掃」「アダプト・サイン」。スマートフォンでもこの順序を保つ。

B-7の図は人物5人、自転車1台、高木1本、低木、車1台、左向きの視線矢印2本を照合。D-2は人物8人、2本の清掃道具、ベンチ、花壇、通路、樹木の位置関係を照合した。清書版は描画を改善したPNGであり、原図と画素・座標の完全一致を保証するものではない。

InDesign「二版」は読み出せた本文・キャプションの文字列も参照した。ただしネイティブ文書の最終レイアウト全体は解析していないため、掲載内容と順序の基準は公開PDFとした。原本と個別の照合記録は公開リポジトリ外に保管している。

B-7・D-2は承認を受け、正式ページへ反映済み。正式ページは、プレビュー表示と検索除外指定を除いて承認済みプレビューと同じ内容で生成した。トップページの既存リンクはそのまま正式URLに向いている。

```sh
python3 scripts/build_keyword.py content/keywords/b-7.json --output b-7-visibility-in-parks.html
python3 scripts/build_keyword.py content/keywords/d-2.json --output d-2-maintenance-participation.html
```

## A-1・C-1の原著照合記録

| 項目 | A-1 ウォーカビリティ | C-1 公共空間に向く窓 |
|---|---|---|
| 掲載箇所 | p.22（PDF内8ページ目） | p.50（同36ページ目） |
| 本文 | 初期Web版の「ウォーカビリティの高い」を原文の「ウォーカビリティのある」に戻した | 原著の全文と一致 |
| 図版 | `p22-zu.tif` を基に再清書・彩色。旧Web版の鉄道端の矢印・独自の建物描写を除いた | `p50-zu.ai` と既存 `c-1-gemini.jpg` を比較して継続使用 |
| 写真 | 原著に掲載なし | `p50-photo1.tif`・`p50-photo2.tif` をsRGBのJPEGへ変換。元写真の内容・順序をPDFと照合 |
| コラム | 「ＴＯＤ：公共交通指向型開発」の全文・出典・元の電球マークを掲載 | 独立したコラムなし |
| キャプション | 原著の図にキャプションなし | 原著の写真キャプション2件を全文掲載。図内の文字2件も保持 |

図の要素の照合は公開した比較ページにも記載した。A-1は徒歩圏3つ・駅3点・道路矢印18本、C-1は人物6人・高木2本・上下階の窓・左向き視線矢印2本と文字を確認した。線、色、人物の服装などの描写は清書版の表現で、原図との画素・座標の完全一致を保証するものではない。

A-1・C-1の本文はInDesign「二版」から読み出せた文字列とも一致した。原著PDFの全掲載要素を基準とし、二版のネイティブ最終レイアウト全体の一致までは未確認。写真・図版はファイル名だけで対応を決めず、元画像とPDFの内容を比較した。

A-1・C-1の正式HTMLと既存の画像は変更していない。改修用の新規画像には別名を使い、承認まではプレビューだけで使用する。原図の比較用画像もWeb用PNGで、編集元ファイルは公開リポジトリに登録しない。
