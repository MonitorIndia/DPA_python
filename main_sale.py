from __builtin__ import file
import datetime
import ftplib
import glob
from multiprocessing import Pool, os
import multiprocessing
import shutil


csv_host = "java.gigya.jp"
user_name = "torchlight"
password = "torgigya9147"
file_path = "/var/www/html/test-tt.gigya.jp/csv/"
csv_files = ['ImageTemplateTest1.csv', "ImageTemplateTest2.csv", "ImageTemplateTest3.csv", "ImageTemplateTest4.csv", "ImageTemplateTest5.csv"]

# pretime
a = datetime.datetime.now()
 
def read_csv(file): 
        print file
        
        
# setup /tmp dir. If it already exists clean it.    
def setup_download_dir():
    cwd = os.getcwd()
    if(os.path.isdir(cwd + "//tmp") == True):
        shutil.rmtree(cwd + "//tmp")
    if(os.path.isdir(cwd + "//tmp") == False):
            os.mkdir(cwd + "//tmp", 0777)
    os.chdir(cwd + "//tmp")
    
def download_csv_files(file):
    print file
    ftp = ftplib.FTP(csv_host) 
    ftp.login(user_name, password) 
    ftp.retrbinary("RETR %s" %file_path+file ,open(file, 'wb').write)
    ftp.quit()
           
        
def main():
    setup_download_dir()
    p = Pool(8)
    p.map(download_csv_files, csv_files)
    print "CSV Downloading Done"
# #     os.chdir(os.getcwd() + "//tmp")
#     _files = glob.glob("*.csv") 
# #     print _files
#     read_csv(_files[0])
#     p = Pool(8)
#     p.map(update_csv,_files[0])
        
main()

b = datetime.datetime.now()
print(b - a)
