import os 
import datetime
import glob
import time
import requests

path = os.getcwd() + '/public_html/exports'

today = datetime.datetime.today()
os.chdir(path) 

while True:
    
    response = requests.get('http://localhost:5000/delete_old_tokens')
    
    for root,directories,files in os.walk(path,topdown=False): 
        for name in files:
            
            t = os.stat(os.path.join(root, name))[8] 
            filetime = today - datetime.datetime.fromtimestamp(t)
    
            if filetime.seconds >= 7200:
                os.remove(os.path.join(root, name))
            
    time.sleep(3600)