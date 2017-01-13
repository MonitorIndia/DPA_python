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
from __builtin__ import range
import shutil
a = datetime.datetime.now()
# total = 1001
total = 5
product_catalog_id = "224411331348696"
access_token = "EAADLKZCtcbPoBAGDMydJ8JiM3jKAoZCdKuRKysGYTYT3Krg2pyMVnLZBabgNJ1LoZAYJQY2AYAlRwKlP46aJHeYB5rZC5sJF95ZCtSpEQ1yU9CiT6KZAKricmlZCu7TZBjxuXlkdqkXW4JDw4s2ZCLlloi8pqVSGqhRd4U5ZBDV8ZCNrvwZDZD"
id_list_file_name = "id_list.txt"

def read_id_list_file():
    json_data = ""
    with open(id_list_file_name) as f:
        for line in f:
            if(line.count > 0):
                json_data+="{'retailer_id':{'eq':'"+line.strip()+"'}},"
    print json_data
    get_products_data(json_data)           
            

def get_products_data(products):
    api_endpoint = "https://graph.facebook.com/v2.8/" 
    fb_graph_url = api_endpoint+product_catalog_id+"/products?fields=image_url,retailer_id,id&filter={'or':["+products+"]}&access_token="+access_token
    all_data = requests.get(fb_graph_url).json()['data']
    cwd = os.getcwd()
    if(os.path.isdir(cwd+"//tmp" ) == True):
        shutil.rmtree(cwd+"//tmp")
    if(os.path.isdir(cwd+"//tmp" ) == False):
            os.mkdir(cwd+"//tmp",0777)
    os.chdir(cwd+"//tmp")
#     print all_data
    count = len(all_data)
    counter = 1
    print "Total "+str(count)+" items"
    for data in all_data:
        print "processing "+str(counter) +" of "+str(count)
        image_url = data['image_url']
        retailer_id = data['retailer_id']
        image_data = requests.get(image_url).content
        os.chdir(cwd+"//tmp")
        open(retailer_id+'.png',"a")
        with open(retailer_id+'.png',"wb") as localFile:
            localFile.write(image_data)
        counter = counter+1

def main():
    read_id_list_file()

main()

print "Done"
sys.stdout.write("\n")
 
b = datetime.datetime.now()
print("Total time taken "+str(b-a))