from bs4 import BeautifulSoup
import requests
import random
import string
import json
import pandas as pd
import time
import re

def get_html(url,session):
    HEADER = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
            "Referer":url,
              "cookie":"bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))
             }
    # values = {'username' : 'cqc',  'password' : 'XXXX' }
    text = session.get(url,headers=HEADER).text
    # req = requests.get(url,headers=HEADER)
    # req.headers
    # req.encoding = 'utf-8'
    # text = req.text
    return text

fp = open("movie_page.json",'r')
movie_page = json.load(fp)
fp.close()

A = list(movie_page.items())
HEADER = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
            "Referer":"movie.douban.com",
              "cookie":"bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))
             }
data = {"username":'',"password":''}
login_url = "https://accounts.douban.com/passport/login"
session = requests.Session()
session.post(login_url,data=json.dumps(data),headers=HEADER)
import time
for j in range(177,196):
    movie,url = A[j]
    dataset = pd.DataFrame(columns=("movie","star","comment"))
    print("extracting {} now".format(movie))
    for rank in ['h','m','l']:
        i = 0
        while i<200:
            try:
                text = get_html(url+"comments/?start="+str(i)+"&limit=20&sort=new_score&status=P&percent_type="+rank,session)
                soup = BeautifulSoup(text,features='lxml')
                star = []
                comments = []
                for comment in soup.find_all(class_="comment"):  
                    star.append(comment.find(class_=re.compile("^allstar"))["class"][0][-2])
                    comments.append(comment.find(class_="short").string)
                tmp_set = pd.DataFrame({
                    "movie":movie,
                    "star":star,
                    "comment":comments
                })
                dataset = dataset.append(tmp_set,ignore_index=True)
            except:
                break
            i += 20
            time.sleep(1)
    print("finish extract {}".format(movie))
    filename = "comment/"+str(j)+".csv"
    dataset.to_csv(filename,encoding='gb18030') 