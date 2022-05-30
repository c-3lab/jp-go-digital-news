# デジタル庁サイト更新情報

* デジタル庁サイトはクロールしづらいためこちらに更新情報を流します。
* 営業日(平日)のみ1日1回更新確認しています。

### コンテンツの説明

* jp-go-digital-news-meeting.csv: 「会議等」の更新情報→https://www.digital.go.jp/councils/
* jp-go-digital-news-news.csv: 「ニュース」の更新情報→https://www.digital.go.jp/news/topics/
* jp-go-digital-news.xlsx: 更新情報のソース(手動更新)

## Technology

* xlsxを手動更新し、github actionsにて自動でxlsx->csv変換を行っています。
* xlsx->csv変換にはxlsx2csvを利用しています。

### xlsx2csvの使い方

```
# インストール
pip3 install xlsx2csv

# csv作成
xlsx2csv -n meeting -f '%Y/%m/%d' jp-go-digital-news.xlsx jp-go-digital-news-meeting.csv
xlsx2csv -n news -f '%Y/%m/%d' jp-go-digital-news.xlsx jp-go-digital-news-news.csv
```

## License

CC0-1.0
