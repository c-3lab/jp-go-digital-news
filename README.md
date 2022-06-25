# デジタル庁サイト更新情報

* デジタル庁サイトはクロールしづらいためこちらに更新情報を流します。
* ~~営業日(平日)のみ1日1回更新確認しています。~~ 更新確認を自動化しました(2022/6/25)。

### コンテンツの説明

* jp-go-digital-news-meeting.csv: 「会議等」の更新情報→https://www.digital.go.jp/council/ /**登録漏れが多数ありましたのですべて登録しました(2022/6/24)**
* jp-go-digital-news-news.csv: 「ニュース」の更新情報→https://www.digital.go.jp/news/ **`/news/topics/`は404になりましたのでURLを変更しました(2022/6/25)**
* ~~jp-go-digital-news.xlsx: 更新情報のソース(手動更新)~~ **xlsxファイルは廃止しました(2022/6/24)。2022年7月1日0時以降に予告なくリポジトリから削除します(2022/6/25)。**

## Technology

* `update.py`
  * Github actionsにて1日数回起動
  * `requests`にて該当ページを検索、`BeautifulSoup4`で`a`タグの`href`のうち該当ページと同じプリフィクスをもつもののみ収集、CSVに追加
  * `git diff`で更新を検知し、更新があれば`git add/commit/push`を行う

## License

CC0-1.0
