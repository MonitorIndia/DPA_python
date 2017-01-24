from __builtin__ import file
import csv
from datetime import datetime
from dateutil import parser
import dateutil
import ftplib
import glob
from multiprocessing import Pool, os
import shutil
from pgmagick import Image, CompositeOperator as co
import requests

csv_host = "java.gigya.jp"
user_name = "torchlight"
password = "torgigya9147"
file_path = "/var/www/html/test-tt.gigya.jp/csv/"
csv_files = ['ImageTemplateTest1.csv', "ImageTemplateTest2.csv", "ImageTemplateTest3.csv", "ImageTemplateTest4.csv", "ImageTemplateTest5.csv"]

# pretime
a = datetime.now()

# read csv files @retrun feed_data. if feed_data is empty it means that file doesn't contain sale_price data
def read_csv(file): 
    reader  = csv.DictReader(open(file))
    headers = reader.fieldnames
    feed_data = []
    if(('sale_price' in headers) and ('sale_price_effective_date' in headers)):
        print file
        for current_row in reader:
            dates  = current_row['sale_price_effective_date']
            dates = map(dateutil.parser.parse, dates.split('/'))
            if((current_row['sale_price']!="") and datetime.now(tz=dates[0].tzinfo) < dates[1]):
                id = current_row['id']
                image_url  =current_row['image_link']
                data = [id,image_url] 
                feed_data.append(data) 
    return feed_data  

# setup /tmp dir. If it already exists clean it.    
def setup_download_dir():
    cwd = os.getcwd()
    if(os.path.isdir(cwd + "//tmp") == True):
        shutil.rmtree(cwd + "//tmp")
    if(os.path.isdir(cwd + "//tmp") == False):
            os.mkdir(cwd + "//tmp", 0777)
    os.chdir(cwd + "//tmp")
    
def download_csv_files(file):
    print "Downloading "+str(file)
    ftp = ftplib.FTP(csv_host) 
    ftp.login(user_name, password) 
    ftp.retrbinary("RETR %s" %file_path+file ,open(file, 'wb').write)
    ftp.quit()
           
# Download images using image_url and save into /tmp dir.
def get_image(obj):
    print "Downloading "+str(obj[1])
    image_data = requests.get(obj[1]).content
    f = open(obj[0] + ".png", "wb")
    f.write(image_data)
    f.close()

# Change downloaded images labels.    
def change_image_labels(obj):
    print "Processing " +obj[0]
    try:
        retailer_id = str(obj[0])
        im = Image(retailer_id + '.png')
        os.chdir("..")
#         new = Image('new_r.png')
        red = Image('off.png')
        im.composite(red, 0, 0, co.OverCompositeOp)
#         im.composite(new, 1, 1, co.OverCompositeOp)
        os.chdir(os.getcwd() + "//tmp")
        im.write(retailer_id + ".png")
    except Exception:
            pass

# function to upload new images
def upload_images(feed_data):
    new_data = []
    for data in feed_data:
        data[1]  = "http://www.google.com/"+data[0]
        new_data.append(data)
    return new_data

# function to write new urls to csv files.
def write_csv(feed_data,_file):
    product_ids = set([product[0] for product in feed_data ])
    data_dict = {}
    for data in feed_data:
        data_dict[data[0]]=data[1]
    reader  = csv.DictReader(open(_file))
    out_file_name = str(_file).replace(".csv", "")
    writer = csv.DictWriter(open(out_file_name+"_updated.csv","wb"),fieldnames=reader.fieldnames)
    writer.writeheader()
    for current_row in reader:
        if current_row['id'] in product_ids:
            current_row['image_link'] = data_dict[current_row['id']]
        writer.writerow(current_row)
    os.remove(_file)
    os.rename(out_file_name + "_updated.csv", _file)    
    
# main function            
def main():
    setup_download_dir()
    print "Downloading CSV Files Start"
    p = Pool(8)
    p.map(download_csv_files, csv_files)
    print "Downloading CSV Files Start"
    _files = glob.glob("*.csv") 
    for _file in _files:
        feed_data = read_csv(_file)
        if feed_data:
            p = Pool(8)
            print "Downlaoding Images Start"
            p.map(get_image,feed_data)
            print "Downlaoding Images End"
            print "Changing image labels Start"
            p = Pool(8)
            p.map(change_image_labels,feed_data)
            print "Changing image labels End"
            print "Uploading images Start"
            data_with_new_urls = upload_images(feed_data)
            print "Uploading images End"
            print "Writng CSV Start"
            write_csv(data_with_new_urls,_file)
            print "Writng CSV End"
            
main()

#post time
b = datetime.now()

# print time difference
print(b - a)
