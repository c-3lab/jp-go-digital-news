# デジタル庁サイト更新情報

デジタル庁サイトはクロールしづらいためこちらに更新情報を流します。
ただし、更新状況については`at your own risk'でお願いします。

* jp-go-digital-news-meeting.csv: 「会議等」の更新情報→ https://digital.go.jp/meeting
* jp-go-digital-news-news.csv: 「ニュース」の更新情報→ https://digital.go.jp/news
* jp-go-digital-news.xlsx: CSVのソース

# Technology

* xlsx->csv変換にはxlsx2csvを使用しています。

```
# インストール
pip3 install xlsx2csv

# csv作成
xlsx2csv -n meeting -f '%Y/%m/%d' jp-go-digital-news.xlsx jp-go-digital-news-meeting.csv
xlsx2csv -n news -f '%Y/%m/%d' jp-go-digital-news.xlsx jp-go-digital-news-news.csv
```

# License

CC0-1.0
