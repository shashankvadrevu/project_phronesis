import ast
import pprint
import requests
import json
import re
import sys
from bs4 import BeautifulSoup


def parse_response(path):
    with open(path, 'r') as f:
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


def parse_product_details(j_soup):
    basic_product_dict = {}
    pattern = "product_"
    product_details = []
    product_dict = {}
    # product_list = []
    for each in j_soup["panels"]:
        if pattern in each.get('panelName') and each.get('panelName') != 'cms_product_details_background':
            html = each.get('text')
            basic_details = html.split("<BR/>")
            product_details.append(basic_details)

    for i, each in enumerate(product_details):
        for subEach in each:
            try:
                basic_each = subEach.split("</b>")
                key1 = (basic_each[0].replace("<b>", ""))
                key1 = key1.replace(":", "")
                value0 = basic_each[1].lstrip(" ")
                soup = BeautifulSoup(value0, "html5lib")
                value1 = soup.get_text()
                basic_product_dict.update({key1: value1})
            except Exception as e:
                pass
    # product_list.append(dict(basic_product_dict))
        key2 = "product_{}".format(i + 1)
        product_dict.update({key2: dict(basic_product_dict)})

    return product_dict


if __name__ == '__main__':

    path = str(sys.argv[1])
    # path = 'D:/project_phronesis/docs/files/recall_list.txt'
    json_respone = parse_response(path)
    # pprint.pprint(json_respone)
    basic_details = parse_basicDetails(json_respone)
    who_what = pasre_cms_who_what_consumer(json_respone)
    # pprint.pprint((who_what))
    product_details = parse_product_details(json_respone)

    pprint.pprint(product_details)
