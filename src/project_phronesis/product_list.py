import os
import requests
import pprint
import re
import csv


def get_url():
    list_list = []
    for i in range(2): #9893
        print(i)
        URL_Search = """https://ndb.nal.usda.gov/ndb/search/list?maxsteps=6&
                        format=&count=&max=25&sort=fd_s&fgcd=&manu=&
                        lfacet=&qlookup=&ds=&qt=&qp=&qa=&qn=&q=&ing=&
                        offset=25&order=asc
                        """.format(i * 25)

        r = requests.get(URL_Search)
        pprint.pprint(r.content)



if __name__ == '__main__':
    get_url()

