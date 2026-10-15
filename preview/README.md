# キーワードページのプレビュー運用

新しいページと修正案は、まず `preview/<既存のページ名>.html` に公開して確認する。承認を得るまでは、正式ページの上書き、トップからのリンク追加、正式ページへの反映を行わない。

A-4の確認用URL：

https://cpted-design-guide.github.io/preview/a-4-permeability.html

## 再生成

リポジトリ直下で実行する。Python標準ライブラリだけで動作する。

```sh
python3 scripts/build_keyword.py content/keywords/a-4.json
```

既定の出力先は `preview/`。本文・掲載順・キャプションは原本と照合した `content/keywords/` のデータを利用し、`templates/keyword.html` と `assets/css/keyword.css` で表示する。

プレビューページには識別表示と `noindex, nofollow` を付ける。ただし、GitHub Pagesとこのリポジトリの内容は公開情報であり、アクセス制限ではない。

## 確認と正式反映

1. 原著PDF・編集データで本文、図版、写真、キャプション、掲載順、コラムの有無を照合する。
2. 図は原図と清書・彩色版を比較し、住宅・道路・人物・視線・動線・矢印・文字を確認する。
3. 公開したプレビューで、画像、PC・スマートフォン表示、リンクを確認する。
4. 利用者の承認後にだけ正式ページを生成・反映し、トップや関連キーワードのリンクを更新する。

`--output` は出力先を明示するためのオプション。正式ページへの出力は別途承認が必要。

公開リポジトリにはWeb表示用に変換した画像だけを追加する。AI、InDesign、TIFF、編集用PDFなどの原著編集データや認証情報は追加しない。
