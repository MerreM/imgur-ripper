#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
import sys
import time
import mimetypes
import os
import glob

mimetypes.init()

proxies = {
    "http": "http://localhost:3128",
    "https": "http://localhost:3128"
}

#"/home/mike/Pictures/Ripped-W/"

ALBUM_FORMAT = "https://imgur.com/a/{album_hash}/"

PAGE_FORMAT = "https://imgur.com/a/{album_hash}/{album_hash}/all/page/{page_number}?scrolled"
## For use with string.format(keyword=param)
def get_images_to_folder(link,folder):
    _, filename = os.path.split(link)
    filename,_ = os.path.splitext(filename)
    files = glob.glob(os.path.join(folder,filename)+"*")
    if files:
        return "File probably already exists : %s " % filename
    resp = requests.get(link,proxies=proxies)
    mime = resp.headers.get("content-type")
    path = os.path.join(folder,filename+mimetypes.guess_extension(mime, strict=True))
    if os.path.exists(path):
        print "%s Already exists!"%filename
        return
    with open(path,"wb") as new_image:
        new_image.write(resp.content)
        print "Got %s" % filename
    time.sleep(5)

def get_images_from_url(url, folder):
    resp = requests.get(url,proxies=proxies)
    soup = BeautifulSoup(resp.content)
    links = []
    for img in soup.find_all("div",class_="post"):
        links.append("http:"+img.a.get("href"))
    if len(links)!=0:
        print "Found %s images" % len(links)
        for link in links:
            get_images_to_folder(link,folder)
        return True
    return False

def main(album_hash, folder):
    album_url = ALBUM_FORMAT.format(album_hash=album_hash)
    count = 1
    while get_images_from_url(album_url, folder):
        album_url = PAGE_FORMAT.format(album_hash=album_hash,page_number=count)
        count+=1


if __name__ == '__main__':
    args = sys.argv

    if len(args) != 3:
        # Print out the help message and exit:
        print ("URL and Folder, for args.")
        exit()
    album_hash = args[1]
    folder = args[2]
    if os.path.exists(folder) and os.path.isdir(folder):
        main(album_hash, folder)