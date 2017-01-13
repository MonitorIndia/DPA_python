from multiprocessing import Pool
import datetime
import requests
import os
import shutil
from pgmagick import Image, CompositeOperator as co

# pretime
a = datetime.datetime.now()

# settings
product_catalog_id = "224411331348696"
access_token = "EAADLKZCtcbPoBAGDMydJ8JiM3jKAoZCdKuRKysGYTYT3Krg2pyMVnLZBabgNJ1LoZAYJQY2AYAlRwKlP46aJHeYB5rZC5sJF95ZCtSpEQ1yU9CiT6KZAKricmlZCu7TZBjxuXlkdqkXW4JDw4s2ZCLlloi8pqVSGqhRd4U5ZBDV8ZCNrvwZDZD"
ids_file = "id_list.txt"
products_limit  = 1000;

#read file which contains retailer_id list and return it's contents.
def read_file(file_name):
    f = open(file_name)
    lines = f.readlines()
    f.close()
    return lines

#call fb api with retailer_id list and return all products data.
def call_fb_api(ids):
    api_endpoint = "https://graph.facebook.com/v2.8/"
    filter_param = "filter={'retailer_id':{'is_any':[" + ','.join("'{0}'".format(w.strip()) for w in ids) + "]}}"
    fields_param = "fields=image_url,retailer_id"
    limit_param = "limit=" + str(products_limit)
    token_param = "access_token=" + access_token
    fb_graph_url = api_endpoint + product_catalog_id + "/products?" + limit_param + "&" + fields_param + "&" + filter_param + "&" + token_param
    print fb_graph_url
    response = requests.get(fb_graph_url).json()
    return response['data']    

#Download images using image_url and save into /tmp dir.
def get_image(obj):
    print "Downloading "+str("'"+obj['retailer_id']+"'")
    image_data = requests.get(obj["image_url"]).content
    f = open(obj["retailer_id"] + ".png", "wb")
    f.write(image_data)
    f.close()

#Change downloaded images labels.    
def change_image_labels(obj):
    print "Processing "+str("'"+obj['retailer_id']+"'")
    try:
        retailer_id = str(obj['retailer_id'])
        im = Image(retailer_id + '.png')
        new = Image('new_r.png')
        red = Image('red.png')
        im.composite(red, 0, 0, co.OverCompositeOp)
        im.composite(new, 1, 1, co.OverCompositeOp)
        im.write(retailer_id + ".png")
    except:
        print "error" + str(obj['retailer_id'])
        pass

def chunks(line_list, n):
    for index in xrange(0, len(line_list), n):
        yield line_list[index:index + n]
 
    
def main():
    lines = read_file(ids_file)
    for chunk in chunks(lines, products_limit):
        products = call_fb_api(chunk)
        print "Downloading Images..."
        p = Pool(8)
        p.map(get_image, products)
        print "Downloading Done"
        print "Processing images..."
        p = Pool(8)
        p.map(change_image_labels, products)
        print "Processing Done"
    
main()

b = datetime.datetime.now()
print(b - a)
