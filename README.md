# デジタル庁サイト更新情報

* デジタル庁サイトの更新情報をCSV追加形式で流します。

## コンテンツの説明

* jp-go-digital-news-meeting.csv: 「会議等」の更新情報→https://www.digital.go.jp/council
* jp-go-digital-news-news.csv: 「ニュース」の更新情報→https://www.digital.go.jp/news

## Technology

* `update.py`
  * Github actionsにて1日数回起動
  * `requests`にて該当ページを検索、`BeautifulSoup4`で`a`タグの`href`のうち該当ページと同じプリフィクスをもつもののみ収集、CSVに追加
  * `git diff`で更新を検知し、更新があれば`git add/commit/push`を行う

## License

CC0-1.0
