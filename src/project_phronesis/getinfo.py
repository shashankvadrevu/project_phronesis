import ast
import pprint
import requests
import json
import re
import sys
from bs4 import BeautifulSoup
import pdb
import re


def parse_response(path):
    with open(path, 'r') as f:
        recall_list = ast.literal_eval(f.read())

    for each in recall_list:
        recall_url = "http://healthycanadians.gc.ca/recall-alert-rappel-avis/api/68624/en".format(
            each)
        r = requests.get(recall_url)
        j_soup = json.loads(r.text)
        basic_details = parse_basicDetails(j_soup)
        panel_details = parse_panel_details(j_soup)
        product_details = parse_product_details(j_soup)
        other_details = parse_other_details(j_soup)
        image_details = parse_image_details(j_soup)
        break

    return "execution complete"


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


# def parse_cms_who_what_consumer(j_soup):
#     cms_who_what_consumer_dict = {}
#     for each in j_soup['panels']:
#         if each.get('panelName') == 'cms_who_what_consumer':
#             html = each.get('text')
#             html_strip = html.replace("\n", "")
#             soup = BeautifulSoup(html_strip, "html5lib")
#             key1 = 'cms_who_what_consumer'
#             value1 = soup.get_text()
#             cms_who_what_consumer_dict.update({key1: value1})

#     return cms_who_what_consumer_dict

def parse_panel_details(j_soup):
    panel_details = {}
    regex_str = 'product_[0-9]+|basic_details|images'
    pattern = re.compile(regex_str)
    for panel in j_soup['panels']:
        if not pattern.match(panel["panelName"]):
            html_content = panel.get('text')
            html_strip = html_content.replace("\n", "")
            soup = BeautifulSoup(html_strip, "html5lib")
            value = soup.get_text()
            panel_details[panel['panelName']] = value
    return panel_details


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


def parse_other_details(j_soup):
    other_details = {}
    keys_list = ['url', 'recallId', 'title', 'start_date', 'date_published']
    for key in keys_list:
        if key in j_soup:
            other_details[key] = j_soup[key]

    return other_details


def parse_image_details(j_soup):
    base_url = 'http://healthycanadians.gc.ca'
    image_details = {}
    for panel in j_soup["panels"]:
        if panel["panelName"] == "images":
            for i, img in enumerate(panel["data"]):
                image_details['img_' + str(i+1)] = {'title': img["title"],
                                                    'fullUrl': base_url+img["fullUrl"]}
    return image_details


if __name__ == '__main__':

    # path = str(sys.argv[1])
    # # path = 'D:/project_phronesis/docs/files/recall_list.txt'
    # json_respone = parse_response(path)
    # # pprint.pprint(json_respone)
    # basic_details = parse_basicDetails(json_respone)
    # who_what = parse_cms_who_what_consumer(json_respone)
    # # pprint.pprint((who_what))
    # product_details = parse_product_details(json_respone)

    # pprint.pprint(product_details)

    path = str(sys.argv[1])
    product_details = parse_response(path)

    pprint.pprint(product_details)
