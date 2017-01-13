from pgmagick import Image, CompositeOperator as co
from multiprocessing import Pool
from multiprocessing import Process
from ftplib import FTP
import datetime
import sys
import requests
import urllib2
import json
import os
a = datetime.datetime.now()
# total = 1001
total = 5
product_catalog_id = "224411331348696"
access_token = "EAADLKZCtcbPoBAGDMydJ8JiM3jKAoZCdKuRKysGYTYT3Krg2pyMVnLZBabgNJ1LoZAYJQY2AYAlRwKlP46aJHeYB5rZC5sJF95ZCtSpEQ1yU9CiT6KZAKricmlZCu7TZBjxuXlkdqkXW4JDw4s2ZCLlloi8pqVSGqhRd4U5ZBDV8ZCNrvwZDZD"
id_list_file_name = "id_list.txt"

def read_id_list_file():
    with open(id_list_file_name) as f:
        for line in f:
            if(line.count > 0):
                print line
                get_products_data(line)
                break
            

def get_products_data(name):
    api_endpoint = "https://graph.facebook.com/v2.8/" 
#     fb_graph_url = api_endpoint+product_catalog_id+"/products?fields=image_url,retailer_id,id&filter={'retailer_id':{'eq':'"+name.strip()+"'}}&access_token="+access_token  
    fb_graph_url = api_endpoint+product_catalog_id+"/products?fields=image_url,retailer_id,id&filter={'or':[{'retailer_id':{'eq':'product-0'}},{'retailer_id':{'eq':'product-1'}}]}&access_token="+access_token
    data = requests.get(fb_graph_url).text
    print data
#     image_url =  data['data'][0]['image_url']
# #     print image_url
#     cwd = os.getcwd()
#     image_data = requests.get(image_url).content
# #     print image_data
#     if(os.path.isdir(os.getcwd()+"//tmp" )== False):
#         os.mkdir(os.getcwd()+"//tmp",0777)
#     os.chdir(os.getcwd()+"//tmp")
#     open(name+'.png',"a")
#     with open(name+'.png',"wb") as localFile:
#         localFile.write(image_data)
#     os.chdir(cwd)

def function(n):
    read_id_list_file()

def multi(n):
    p = Pool(8)
    p.map(function, range(1,n))

def main():
#     multi(total)
    function(total)

main()

sys.stdout.write("\n")
 
b = datetime.datetime.now()
print(b-a)