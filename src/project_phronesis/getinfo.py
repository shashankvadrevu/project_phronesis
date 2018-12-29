import ast
import pprint
import requests
import json
import sys
import pdb
import random
import parseResponse
import time
import datetime

"""
Added a parse script

"""


def parse_response(path):

    with open(path, 'r') as f:
        recall_list = ast.literal_eval(f.read())
        random.seed(4)
        recall_list_200 = random.sample(recall_list, 10)

    list_response = []
    recall_details_dict = {}

    for each in recall_list:
        recall_url = "http://healthycanadians.gc.ca/recall-alert-rappel-avis/api/{}/en".format(
            each)
        r = requests.get(recall_url)
        j_soup = json.loads(r.text)

        basic_details = parseResponse.parse_basicDetails(j_soup)
        panel_details = parseResponse.parse_panel_details(j_soup)
        product_details = parseResponse.parse_product_details(j_soup)
        other_details = parseResponse.parse_other_details(j_soup)
        image_details = parseResponse.parse_image_details(j_soup)
        basic_details.update(other_details)

        start_date = basic_details.get("start_date")
        start_date = time.strftime(
            "%a %d %b %Y %H:%M:%S", time.gmtime(start_date))
        basic_details["start_date"] = start_date

        parsed_response = {}
        parsed_response.update({"basic_details": basic_details})
        parsed_response.update({"panel_details": panel_details})
        parsed_response.update({"product_details": product_details})
        # parsed_response.update({"other_details": other_details})
        parsed_response.update({"image_details": image_details})

        key1 = each
        value1 = dict(parsed_response)

        recall_details_dict.update({key1: value1})

        list_response.append(dict(recall_details_dict))

        # break

    # with open('recall_randon_200.txt', 'w') as outfile:
    #     json.dump(list_response, outfile)

    return list_response


if __name__ == '__main__':
    path = str(sys.argv[1])
    recall_details_list = parse_response(path)
    # print()
    pprint.pprint(recall_details_list)
    # pprint.pprint(dateConvert(recall_details_list))
