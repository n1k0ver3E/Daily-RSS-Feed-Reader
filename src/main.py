import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from workflow import Workflow, web, ICON_WARNING
from datetime import datetime
import json, time
import sys, os

import urllib, requests
import xml.etree.ElementTree as ET


class RSSParser(object):
    # def __init__(self,url):
    #     self.url = url

    def format_date(self, date_):
        """pubdate formatter, parse format based on RSS 2.0 pubdate format.
        parse format can be modified on variable rss_pubdate_fmt.

        Args:
            date_
        Return:
            date with new format
        """

        rss_pubdate_fmt = "%a, %d %b %Y %H:%M:%S"
        new_date_fmt = "%Y-%m-%d %H:%M:%S"
        date_ = " ".join(date_.split(" ")[:-1])
        return datetime.strptime(date_, rss_pubdate_fmt).strftime(new_date_fmt)

    def return_rss_list(self):
        """Fetch List with title and link from config.json

        Return:
            List, rss_subscribe_list
            for example:[{u'link': u'https://sspai.com/feed', u'title': u'sspai'}, {u'link': u'https://rsshub.app/ifanr/app', u'title': u'ifanr'}]

        Raises:
            Exception: Return False. An error occurred when read config.json
        """

        with open('./config.json', 'r') as f:
            data = json.load(f)
            try:
                rss_subscribe_list = data[u'rss_subscribe']
                return rss_subscribe_list
            except Exception as e:
                return False

    def return_xml_item(self):
        """Fetch Final result list with title, link, source, date

        Return:
            result
            for example: [{'date': '2021-02-04 09:07:33', 'source': u'sspai', 'link': 'https://sspai.com/post/64927', 'title': u'\u6d3e\u65e9'},{...}]

        Raises:
            Exception: Return False. An error occurred when parse xml from rss_subscribe_list.link
        """

        result = list()
        rss_list = self.return_rss_list()
        try:
            for rss in rss_list:
                rss_temp = self.parse_xml_text(rss[u'title'], rss[u'link'])
                result = result + rss_temp
            return result
        except Exception as e:
            return False

    def parse_xml_text(self, source, url):
        """parse xml content from certain source and save to list.

        Args:
            source: RSS source, read from config.json
            url: RSS link, read from config.json


        Return:
            res
            for example: [{'date': '2021-02-04 09:07:33', 'source': u'sspai', 'link': 'https://sspai.com/post/64927', 'title': u'\u6d3e\u65e9'},{...}]
        """

        res = list()
        text = requests.get(url).content
        text = ET.fromstring(text)
        for item in text.iterfind('channel/item'):
            temp = dict()
            temp["title"] = item.findtext('title')
            temp["date"] = self.format_date(item.findtext('pubDate'))
            temp['source'] = source
            temp["link"] = item.findtext("link")
            res.append(temp)
        return res


def main(wf):
    arguments = wf.args
    # print(arguments)
    args = ''.join(arguments)

    if args:
        args = wf.args[0].strip(" ").split(" ")

        if len(args) == 1 and args[0] == u"help":
            """
            :Command: RSS help
            """
            wf.add_item(
                title="rss",
                subtitle="Display contents from all RSS sources.",
                icon='icon/ICON_INFO.png'
            )
            wf.add_item(
                title="rss list",
                subtitle="List all RSS sources.",
                icon='icon/ICON_INFO.png'
            )
            wf.add_item(
                title="rss open",
                subtitle="Open config.json to add new source.",
                icon='icon/ICON_INFO.png',
                valid="yes",
                arg="open"

            )
            wf.add_item(
                title="rss <source_name>  eg: rss sspai",
                subtitle="List contents of certain rss source.",
                icon='icon/ICON_INFO.png'
            )
        elif len(args) == 1 and args[0] == "list":
            """
            :Command: RSS list
            """
            rssParser = RSSParser()
            rssList = rssParser.return_rss_list()
            # print(rssList)
            for item in rssList:
                wf.add_item(
                    title="Source: " + item[u'title'],
                    subtitle="Link: " + item[u'link'],
                    valid="",
                    icon="",
                    arg=""
                )
        elif len(args) == 1 and args[0] == "open":
            """
            :Command: RSS open
            """
            wf.add_item(
                title="Open config.json to add new source",
                icon='icon/ICON_SYNC.png',
                valid="yes",
                arg="open"

            )


        else:
            rss_parser = RSSParser()
            rss_list = rss_parser.return_rss_list()
            rssSource = [i[u'title'] for i in rss_list]
            arg_source = arguments[0]

            if arg_source in rssSource:
                """
                :Command: RSS <source_name>
                """
                for i in rss_list:
                    if i['title'] == arg_source:
                        rss_url = i['link']
                result = rss_parser.parse_xml_text(arg_source, rss_url)
                for item in result:
                    wf.add_item(
                        title=item["title"],
                        subtitle="Source: " + item["source"] + "          PubDate: " + item["date"],
                        valid='yes',
                        arg=item["link"]
                    )
            else:
                """
                Catch command exception
                """
                wf.add_item(
                    title="RSS source not found at ./config.json",
                    valid="",
                    icon='icon/ICON_ERROR.png',
                    arg=""
                )

    else:
        rss_parser = RSSParser()
        result = wf.cached_data('total', rss_parser.return_xml_item, max_age=300)
        if result:
            ordered_result = sorted(result, key=lambda x: x["date"], reverse=True)
            for item in ordered_result:
                wf.add_item(
                    title=item["title"],
                    subtitle="Source: " + item["source"] + "          PubDate: " + item["date"],
                    valid='yes',
                    arg=item["link"]
                )
        else:
            wf.add_item(
                title="SourceError : RSS source cannot be found or parsed successfully.",
                subtitle="Please input 'rss open' to check configuration."
            )
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
