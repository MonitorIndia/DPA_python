from __builtin__ import file
import datetime
import gc
import glob
from multiprocessing import Pool
import os
import shutil
import subprocess
import urllib
from pgmagick import Image, CompositeOperator as co
import requests
import urlparse
import re
import csv


# pretime
a = datetime.datetime.now()

# settings
product_catalog_id = "224411331348696"
access_token = "EAADLKZCtcbPoBAGDMydJ8JiM3jKAoZCdKuRKysGYTYT3Krg2pyMVnLZBabgNJ1LoZAYJQY2AYAlRwKlP46aJHeYB5rZC5sJF95ZCtSpEQ1yU9CiT6KZAKricmlZCu7TZBjxuXlkdqkXW4JDw4s2ZCLlloi8pqVSGqhRd4U5ZBDV8ZCNrvwZDZD"
ids_file = "id_list.txt"
api_endpoint = "https://graph.facebook.com/v2.8/"
token_param = "access_token=" + access_token
products_limit = 1000;

# read file which contains retailer_id list and return it's contents.
def read_file(file_name):
    f = open(file_name)
    lines = f.readlines()
    if(len(lines) < 1):
        raise "File doesn't contains any data. At least one retailer-id is required."
    f.close()
    global prouct_limit
    prouct_limit = len(lines)
    print "Total " + str(len(lines)) + " items"
    return lines

# call fb api with retailer_id list and return all products data.
def call_fb_api(ids):
    filter_param = "filter={'retailer_id':{'is_any':[" + ','.join("'{0}'".format(w.strip()) for w in ids) + "]}}"
    print filter_param
    fields_param = "fields=image_url,retailer_id"
    limit_param = "limit=" + str(prouct_limit)
    fb_graph_url = api_endpoint + product_catalog_id + "/products?" + limit_param + "&" + fields_param + "&" + filter_param + "&" + token_param
#     print fb_graph_url
    response = requests.get(fb_graph_url).json()
    return response['data']    

# Download images using image_url and save into /tmp dir.
def get_image(obj):
    print "Downloading " + str("'" + obj['retailer_id'] + "'")
    image_data = requests.get(obj["image_url"]).content
    f = open(obj["retailer_id"] + ".png", "wb")
    f.write(image_data)
    f.close()

# setup /tmp dir. If it already exists clean it.    
def setup_download_dir():
    cwd = os.getcwd()
    if(os.path.isdir(cwd + "//tmp") == True):
        shutil.rmtree(cwd + "//tmp")
    if(os.path.isdir(cwd + "//tmp") == False):
            os.mkdir(cwd + "//tmp", 0777)
    os.chdir(cwd + "//tmp")

# Change downloaded images labels.    
def change_image_labels(obj):
        print "Processing " + str("'" + obj['retailer_id'] + "'")
        try:
            retailer_id = str(obj['retailer_id'])
            im = Image(retailer_id + '.png')
            os.chdir("..")
            new = Image('new_r.png')
            red = Image('red.png')
            im.composite(red, 0, 0, co.OverCompositeOp)
            im.composite(new, 1, 1, co.OverCompositeOp)
            os.chdir(os.getcwd() + "//tmp")
            im.write(retailer_id + ".png")
#             im.write(retailer_id+"_comp.png")
#             os.remove(retailer_id+'.png')
        except Exception:
            pass
 
def chunks(line_list, n):
    for index in xrange(0, len(line_list), n):
        yield line_list[index:index + n]   

def get_all_csv_feeds():
#     setup_download_dir()
    fields_param = "fields=id,file_name,name,schedule"
    fb_graph_url = api_endpoint + product_catalog_id + "/product_feeds?" + fields_param + "&" + "&" + token_param
#     print fb_graph_url
    response = requests.get(fb_graph_url).json()
    all_data = response['data']
    return all_data
#     download_csv_files(all_data[0])
    
    
def download_csv_files(data):
    file_name = data['file_name'].replace(" ", "_")
    csv_url = data['schedule']['url']
    print "Downloading " + csv_url
    response = requests.get(csv_url).text
#     print response
    f = open(file_name + ".csv", "wb")
    f.write(response)
    f.close()

def update_csv(products):
#     print products
#     for product in products:
#         retailer_id = product['retailer_id']
#         image_url = product['image_url']
#         for file in glob.glob("*.csv"): 
#             print file
#             reader  = csv.DictReader(open(file))
#             writer = csv.DictWriter(open("demo.csv","wb"))
# #             i=0
#             for row in reader:
# #                 print row['id']
# #                 print row['image_link']
# #                 print row
#                 if(retailer_id == row['id']):
#                     row['image_link']='rajsharma'
#                 i+=1
    
    print products
    image_urls = []
    for product in products:
        print product
        decoded_url = urllib.unquote(product['image_url'])
        url = re.search('&url.*(.png)', decoded_url).group()
        print url
        url = re.search('&url.*(.png)', decoded_url).group(0).split("=")[1]
        image_urls.append(url)
    print image_urls
    for file in glob.glob("*.csv"): 
        print file
        out_file_name = str(file).replace(".csv", "")
        command  = "sed '"+";".join("{0}".format("s,"+w.strip()+",rajsharma1612,g") for w in image_urls)+"' "+file+" > "+out_file_name+"_updated.csv"
        print command
        subprocess.call([command], shell=True)
        os.rename(out_file_name + "_updated.csv", file)
        

def main():
    lines = read_file(ids_file)
    setup_download_dir()
    for chunk in chunks(lines, products_limit):
        products = call_fb_api(chunk)
        print "Downloading Images..."
#         p = Pool(8)
#         p.map(get_image, products)
        print "Downloading Done"
        print "Processing images..."
#         p = Pool(8)
#         p.map(change_image_labels, products)
        print "Processing Done"
        all_data = get_all_csv_feeds()
#         print all_data
#         p = Pool(8)
#         p.map(download_csv_files,all_data)
        download_csv_files(all_data[4])
        update_csv(products)
#         p = Pool(8)
#         p.map(update_csv,products)
#         memory release
        del products
        gc.collect()
        
main()

b = datetime.datetime.now()
print(b - a)
