import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from workflow import Workflow, web, ICON_WARNING
from datetime import datetime
import json, time
import sys,os

import urllib,requests
import xml.etree.ElementTree as ET

class RSSParser(object):
    # def __init__(self,url):
    #     self.url = url

    def format_date(self, date_):
        rss_pubdate_fmt = "%a, %d %b %Y %H:%M:%S"
        new_date_fmt = "%Y-%m-%d %H:%M:%S"
        date_ = " ".join(date_.split(" ")[:-1])
        return datetime.strptime(date_, rss_pubdate_fmt).strftime(new_date_fmt)

    def return_rss_list(self):
        """Return rssSubscribeList
        :return: [{u'link': u'https://sspai.com/feed', u'title': u'sspai'}, {u'link': u'https://rsshub.app/ifanr/app', u'title': u'ifanr'}]
        """
        
        with open('./config.json', 'r') as f:
            data = json.load(f)
            try:
                rssSubscribeList = data[u'rss_subscribe']
                # print("rssSubscribeList", rssSubscribeList)
                return rssSubscribeList
            except Exception as e:
                return False
   
    def parse_xml_text(self,source, url):
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
        
    def return_xml_item(self):
        result = list()
        rssList = self.return_rss_list()   
        try:
            for rss in rssList:
                # rssTemp = wf.cached_data('total', lambda: self.parse_xml_text(rss[u'title'], rss[u'link']), max_age=300)
                rssTemp = self.parse_xml_text(rss[u'title'], rss[u'link'])
                result = result + rssTemp
            return result
        except Exception as e:
            return False
        
# def sorted_rssList_by_date():
    
def main(wf):
    url = "https://www.ifanr.com/feed"
    url = "https://rsshub.app/v2ex/topics/hot"
    arguments = wf.args
    # print(arguments)
    args = ''.join(wf.args)
    
    if args:
        args = wf.args[0].strip(" ").split(" ")
        
        if len(args) == 1 and args[0] == u"help":
            wf.add_item(
                title = "rss",
                subtitle = "Display contents from all RSS sources.",
                icon = 'icon/ICON_INFO.png'
            )
            wf.add_item(
                title = "rss list",
                subtitle = "List all RSS sources.",
                icon = 'icon/ICON_INFO.png'
            )
            wf.add_item(
                title = "rss open",
                subtitle = "Open config.json to add new source.",
                icon = 'icon/ICON_INFO.png',
                valid = "yes",
                arg = "open"
                
            )
            wf.add_item(
                title = "rss <source_name>  eg: rss sspai",
                subtitle = "List contents of certain rss source.",
                icon = 'icon/ICON_INFO.png'
            )
        elif len(args) == 1 and args[0] == "list":
            rssParser = RSSParser()
            rssList = rssParser.return_rss_list()
            # print(rssList)
            for item in rssList:
                wf.add_item(
                    title = "Source: " + item[u'title'],
                    subtitle = "Link: " + item[u'link'],
                    valid = "",
                    icon = "",
                    arg = ""
                    )
        elif len(args) == 1 and args[0] == "open":
            wf.add_item(
                title = "Open config.json to add new source",
                icon = 'icon/ICON_SYNC.png',
                valid = "yes",
                arg = "open"
                
            )
            
            
        else:
            rssParser = RSSParser()
            rssList = rssParser.return_rss_list()
            rssSource = [i[u'title'] for i in rssList]
            arg_source = arguments[0]
            
            if arg_source in rssSource:
                for i in rssList:
                    if i['title'] == arg_source:
                        rss_url =  i['link']
                result = rssParser.parse_xml_text(arg_source, rss_url)
                # result = wf.cached_data('data', lambda: rssParser.parse_xml_text(arg_source, rss_url), max_age=300)
                for item in result:
                    wf.add_item(
                        title = item["title"],
                        subtitle = "Source: " + item["source"] + "          PubDate: " + item["date"],
                        valid='yes',
                        arg = item["link"]
                    )
            else:
                wf.add_item(
                    title = "RSS source not found at ./config.json",
                    valid = "",
                    icon = 'icon/ICON_ERROR.png',
                    arg = ""
                    )
            
    else:
        rssParser = RSSParser()
        # result = rssParser.return_xml_item()
        result = wf.cached_data('total', rssParser.return_xml_item, max_age=300)
        # print("resultttttt:",result)
        if result:
            orderedResult = sorted(result,key=lambda x:x["date"],reverse=True)
            for item in orderedResult:
                wf.add_item(
                    title = item["title"],
                    subtitle = "Source: " + item["source"] + "          PubDate: " + item["date"],
                    valid='yes',
                    arg = item["link"]
                    )
        else:
            wf.add_item(
                title = "SourceError : RSS source cannot be found or parsed successfully.",
                subtitle = "Please input 'rss open' to check configuration."
                )
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    wf.settings['key111'] = {'key2': 'value'}
    log = wf.logger
    sys.exit(wf.run(main))