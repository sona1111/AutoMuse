OUT_DIR = 'C:/Users/sunli/Downloads/gesture_drawings/gesture_drawings/single/img'
listfile = 'C:/Users/sunli/Downloads/gesture_drawings/gesture_drawings/links_to_single.txt'

import os
import requests

with open(listfile, 'r') as f:
    for line in f:
        link, outname = line.replace('\n', '').split(' ')
        outpath = OUT_DIR + '/' + outname
        if not os.path.exists(outpath):
            print(outpath)
            try:
                r = requests.get(link, allow_redirects=True)
            except:
                print('err')
                continue
            with open(os.path.join(OUT_DIR, outname), 'wb') as fw:
                fw.write(r.content)
    
