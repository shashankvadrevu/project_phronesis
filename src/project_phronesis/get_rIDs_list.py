import os
import requests
import pprint
import re
import csv


def get_url():
    list_list = []
    for i in range(349):
        URL_Search = """http://healthycanadians.gc.ca/recall-alert-rappel-avis/search-recherche/simple?s=&plain_text=&f_mc=1&js_en=&page=10&per_page={}""".format(
            i * 10)
        r = requests.get(URL_Search)
        output_response = r.content
        content = output_response.decode('utf-8')
        pattern_inspection = "/recall-alert-rappel-avis/inspection/" + \
            "[0-9][0-9][0-9][0-9]" + "/" + \
            "[0-9][0-9][0-9][0-9][0-9][a-z]" + "-eng.php"
        inspection = re.findall(pattern_inspection, content)
        list_list.append(list(inspection))

        pattern_hc = "/recall-alert-rappel-avis/hc-sc/" + \
            "[0-9][0-9][0-9][0-9]" + "/" + \
            "[0-9][0-9][0-9][0-9][0-9][a-z]" + "-eng.php"
        hc_sc = re.findall(pattern_hc, content)
        list_list.append(list(hc_sc))

    url_list = [item for sublist in list_list for item in sublist]

    return url_list


def get_r_id(url_list):
    recall_list = []
    for each in url_list:
        split1 = each.split("/")[-1]
        split2 = split1.split("-")[0][0:5]
        recall_list.append(split2)
        recall_list.sort()
    with open("recall_list.txt", 'w') as resultFile:
        resultFile.write(str(recall_list))
    print(len(recall_list))
    return recall_list


if __name__ == '__main__':
    url_list = get_url()
    r_id = get_r_id(url_list)
    print(r_id)
