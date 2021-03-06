# -*- coding: utf-8 -*-
"""
Created on Wed May 21 10:03:56 2019

Spyder python3.7.1

@author:  
"""

import requests
import codecs
import os
import time
import datetime
from pyquery import PyQuery as pq

def git_add_commit_push(date, filename):
    cmd_git_add = 'git add .'
    cmd_git_commit = 'git commit -m "{date}"'.format(date=date)
    cmd_git_push = 'git push -u origin master'

    os.system(cmd_git_add)
    os.system(cmd_git_commit)
    os.system(cmd_git_push)
    
def createMarkdown(date, filename):
    with open(filename, 'w') as f:
        f.write("### " + date + "\n")

def scrape(language, filename):

    HEADERS = {
        'User-Agent'		: 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Accept'			: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding'	: 'gzip, deflate, br',
        'Accept-Language'	: 'zh-CN,zh;q=0.9'
    }

    url = 'https://github.com/trending/{language}'.format(language=language) + '?since=daily'
    r = requests.get(url, headers=HEADERS)
    assert r.status_code == 200
    print(url)
    
    # print(r.encoding)
    d = pq(r.content)
   
    items = d('ol.repo-list li')
#     <ol class="repo-list">
    
    # codecs to solve the problem utf-8 codec like chinese
    with codecs.open(filename, "a", "utf-8") as f:
        if language == 'C%23':
            language ='C#'
        f.write('\n#### {language}\n'.format(language=language))

        for item in items:
            i = pq(item)
            title = i("h3 a").text()
#            owner = i("span.prefix").text()
#            print(owner)
            description = i("p.col-9").text()
            url = i("h3 a").attr("href")
            url = "https://github.com" + url
            # ownerImg = i("p.repo-list-meta a img").attr("src")
            # print(ownerImg)
            f.write(u"* [{title}]({url}):{description}\n".format(title=title, url=url, description=description))
        f.flush()
        print('save success')


def job():

    strdate = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = '{date}.md'.format(date=strdate)

    # create markdown file
    createMarkdown(strdate, filename)

    # write markdown
    scrape('python', filename)
    time.sleep(3)
    scrape('c', filename)
    time.sleep(3)
    scrape('C++', filename)
    time.sleep(3)
    scrape('dart', filename)
    time.sleep(3)
    scrape('java', filename)
    time.sleep(3)
    scrape('javascript', filename)
    time.sleep(3)
    scrape('go', filename)
    time.sleep(3)
    scrape('objective-c', filename)
    time.sleep(3)
    scrape('swift', filename)
    time.sleep(3)
    scrape('C%23', filename)
    

if __name__ == '__main__':
    
    job()
    print('The script has finished running')
      
