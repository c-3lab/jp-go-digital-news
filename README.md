# デジタル庁サイト更新情報

* デジタル庁サイトの更新情報をCSV追加形式で流します。

## トピックス

* **本サイトでの自動更新を終了しプロジェクトをアーカイブします。(2024/10/27(日)16時30分)**
  * 自動更新終了日時：2025年1月1日午前0時以降(予定)→**実施(2025年1月2日18時)**
  * プロジェクトアーカイブ日時：同日同時刻以降(予定)
* 以下の理由によりCSVの洗い替えを実施しました。(2023/1/23(月)9時30分)
  * 「会議等」について、フォルダ構成の変更に追従できておらず会議状況更新が漏れていた( https://github.com/c-3lab/jp-go-digital-news/issues/5 対応)
  * 「ニュース」について、過去と同一URLで更新されたお知らせが漏れていた( https://github.com/c-3lab/jp-go-digital-news/issues/6 対応)
  * 「調達情報」について、件名がうまく取れていなかった
  * 日付、説明については大幅な変更あり

## コンテンツの説明

* jp-go-digital-news-meeting.csv: 「会議等」の更新情報→https://www.digital.go.jp/council
* jp-go-digital-news-news.csv: 「ニュース」の更新情報→https://www.digital.go.jp/news
* jp-go-digital-news-procurement.csv: 「調達情報」の更新情報→https://www.digital.go.jp/procurement (対象リンクはhttps://www.p-portal.go.jp/)

## Technology

* `update.py`
  * Github actionsにて1日数回起動
  * `requests`にて該当ページを検索、`BeautifulSoup4`で`a`タグの`href`のうち該当ページと同じプリフィクスをもつもののみ収集、CSVに追加
  * `git diff`で更新を検知し、更新があれば`git add/commit/push`を行う

## License

CC0-1.0
