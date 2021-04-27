# Daily-RSS-Feed-Reader
An alfred workflow to display content of RSS feeds Directly.

---

## 0x00 Install
- Download `Daily.RSS.Feed.Reader.alfredworkflow` from [release](https://github.com/PYF0311/Daily-RSS-Feed-Reader/releases/tag/v1.0.0).
- Double click to import.

## 0x01 Features
- Directly display the content of RSS feeds.
- Easily manage and customize rss feeds.

## 0x02 Instructions
- ``rss`` : Display the contents from all RSS feeds

  ![](./img/rss.gif)

  

- ``rss [source_name] `` : Display the contents from certain RSS feed. eg: ``rss sspai`` 

  ![](./img/rss_sourceName.gif)

- ``rss help`` : Display all available commands

  ![](./img/rss_help.gif)

- ``rss open`` : Open ``./config.json`` to manage RSS feeds

  ![](./img/rss_open.gif)

## 0x03 Customization
- Default app to open ``config.json`` is TextEdit, which can be modified from ``Alfred Preferences``.
- The element ``pubDate`` in RSS conform to the specification of RFC 822. Format and example can be found from [RSS 2.0 specification](https://validator.w3.org/feed/docs/rss2.html). 
- When the format does not match, it will cause a parsing error. It can be customized from [here](https://github.com/PYF0311/Daily-RSS-Feed-Reader/blob/74ffb951aeeb31218d79a3543fdfbc92d7425742/src/main.py#L29).

## 0x04 todo
- 联动chrome，增加「添加到reading list」功能

