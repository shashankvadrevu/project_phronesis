import pprint
import requests
import json
import boto3
import time


def updateRecent_CA():

    dynamodb = boto3.resource(
        'dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")
    table = dynamodb.Table("Recent_15Recall_CAN")
    response_ddb = table.scan()

    recall_15_ddb = []

    for eachItem in response_ddb['Items']:
        recall_15_ddb.append(eachItem.get('recallId'))

    recent_url = "http://healthycanadians.gc.ca/recall-alert-rappel-avis/api/recent/en"
    r = requests.get(recent_url)
    j_soup = json.loads(r.text)
    recall_15_url = []
    for i, each in enumerate(j_soup['results']['FOOD']):
        recall_15_url.append(each['recallId'])

    new_recallId = list(set(recall_15_url) - set(recall_15_ddb))
    print(new_recallId)

    # count_new = len(new_recallId)
    # print(recall_15_ddb)
    # print(count_new)
    # print(recall_15_ddb[:-count_new])
    ts = int(time.time())

    for i, each in enumerate(j_soup['results']['FOOD']):
        if (each['recallId']) in new_recallId:
            table.put_item(
                Item={
                    'recallId': each['recallId']
                    # 'title': each['title'],
                    # 'category': each['category'],
                    # 'date_published': each['date_published'],
                    # 'url': each['url'],
                    # 'timestamp': ts
                })

    scan_db = table.scan()

    recall_scan_db = []
    for each in scan_db.get('Items'):
        recall_scan_db.append(each.get('recallId'))

    for each_json in j_soup['results']['FOOD']: 
    	for each in recall_scan_db:
    		if (each_json['recallId']) == each:
    			table.update_item(
                Item={
                    # 'recallId': each['recallId']
                    'title': each_json['title'],
                    'category': each_json['category'],
                    'date_published': each_json['date_published'],
                    'url': each_json['url'],
                    'timestamp': ts
                })





    # table.update_item(
    #                 Key={
    #                     'recallId': Items['recallId']
    #                 },
    #                 UpdateExpression='SET {} = :val1'.format(Key),
    #                 ExpressionAttributeValues={
    #                     ':val1': someValue1
    #                 }
    #             )

    return


if __name__ == '__main__':
    # path = str(sys.argv[1])
    updateRecent_CA()


# '68458'
