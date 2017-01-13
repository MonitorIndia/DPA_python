from pgmagick import Image, CompositeOperator as co
from multiprocessing import Pool
from multiprocessing import Process
from ftplib import FTP
import datetime
import sys

a = datetime.datetime.now()
toolbar_width = 40
total = 1001

#setup toolbar
sys.stdout.write("[%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width + 1))

def function(n):
    im = Image('http://gigya.jp/dpa/' + str(n) + '.png')
    new = Image('http://test-tt.gigya.jp/dpa/new_r.png')
    red = Image('http://test-tt.gigya.jp/dpa/red.png')
    im.composite(red, 0, 0, co.OverCompositeOp)
    im.composite(new, 1, 1, co.OverCompositeOp)
    im.write('midalort_logo_1024_' + str(n) + '_comp.png')
    ftp = FTP('java.gigya.jp')
    ftp.login('torchlight','torgigya9147')
    ftp.storbinary('STOR midalort_logo_1024_' + str(n) + '_comp.png', open('midalort_logo_1024_' + str(n) + '_comp.png', 'rb'))
    ftp.quit()
    if n % int(total / toolbar_width) == 0:
        sys.stdout.write("-")
        sys.stdout.flush()

def multi(n):
    p = Pool(8)
    p.map(function, range(1,n))

def main():
    multi(total)

main()

sys.stdout.write("\n")
 
b = datetime.datetime.now()
print(b-a)

