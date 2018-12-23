import ast
import pprint
import requests
import json
import re
from bs4 import BeautifulSoup


def parse_response():
    with open('D:/project_phronesis/docs/files/recall_list.txt', 'r') as f:
        recall_list = ast.literal_eval(f.read())

    for each in recall_list:
        recall_url = "http://healthycanadians.gc.ca/recall-alert-rappel-avis/api/{}/en".format(
            each)
        r = requests.get(recall_url)
        j_soup = json.loads(r.text)
        break

    return j_soup


def parse_basicDetails(j_soup):
    for each in j_soup['panels']:
        if each.get('panelName') == 'basic_details':
            html = each.get('text')
            basic_details = html.split("<BR/>")
            basic_details_dict = {}
            for each in basic_details:
                try:
                    basic_each = each.split("</b>")
                    key1 = (basic_each[0].replace("<b>", ""))
                    key1 = key1.replace(":", "")
                    value1 = basic_each[1].lstrip(" ")
                    basic_details_dict.update({key1: value1})
                except Exception as e:
                    pass
    return basic_details_dict


def pasre_cms_who_what_consumer(j_soup):
    cms_who_what_consumer_dict = {}
    for each in j_soup['panels']:
        if each.get('panelName') == 'cms_who_what_consumer':
            html = each.get('text')
            html_strip = html.replace("\n", "")
            soup = BeautifulSoup(html_strip, "html5lib")
            key1 = 'cms_who_what_consumer'
            value1 = soup.get_text()
            cms_who_what_consumer_dict.update({key1: value1})

    return cms_who_what_consumer_dict


if __name__ == '__main__':
    json_respone = parse_response()
    pprint.pprint(json_respone)
    basic_details = parse_basicDetails(json_respone)
    who_what = pasre_cms_who_what_consumer(json_respone)
    pprint.pprint((who_what))
