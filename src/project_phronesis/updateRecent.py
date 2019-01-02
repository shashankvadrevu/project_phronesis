import pprint
import requests
import json
import ast


def updateRecent_CA(path):
    recent_url = "http://healthycanadians.gc.ca/recall-alert-rappel-avis/api/recent/en"
    r = requests.get(recent_url)
    j_soup = json.loads(r.text)

    try:
        with open(path, 'r') as f:
            recent_15_list = ast.literal_eval(f.read())
    except Exception as e:
        pass

    if 'recent_15_list' not in locals():
        recent_15_list = []

    for each in (j_soup['results']['FOOD']):
        if (each['recallId']) not in recent_15_list:
            recent_15_list.append(each['recallId'])

    with open("recall_list_15.txt", 'w') as resultFile:
        resultFile.write(str(recent_15_list))

    return print("List Updated")


if __name__ == '__main__':
    # path = str(sys.argv[1])
    path = "D:/project_phronesis/src/project_phronesis/recall_list_15.txt"
    updateRecent_CA(path)


# '68458'
