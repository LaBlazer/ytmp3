import logging
import requests
import sys
import inspect
from os import path
from threading import Thread
from youtube_dl import YoutubeDL
from ytsearch import ytsearch

class ytmp3(object):
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'ffmpeg_location': path.join(path.dirname(path.abspath(inspect.stack()[0][1])), "ffmpeg")
    }

    def __init__(self):
        self.log = logging.getLogger("ytmp3")
        ytmp3.options["logger"] = self.log
        self.yts = ytsearch()
        self.ytd = YoutubeDL(ytmp3.options)

    def _load_file(self, filename):
        pass

    def search(self, query):
        if not isinstance(query, str):
            raise Exception("query must be a string type")

        return self.yts.search(query)

    def download(self, video_ids):
        if not isinstance(next(iter(video_ids), None), str):
            raise Exception("video ids must be a list of strings type")
        
        self.ytd.download(video_ids)

    def search_and_download(self, query, callback):
        if not callable(callback):
            raise Exception("callback must be a callable object")
        
        results = self.search(query)

        index = 0
        if len(results) > 0:
            index = callback(results)

        if index >= 0 and index < len(results):
            self.log.info(f"Downloading '{results[index].get('title')}'...")
            self.download([results[index].get('id')])
            self.log.info(f"Done!")
        else:
            raise Exception("callback returned invalid index") 
        
    def read_and_download(self, filename, delimeter = '\n'):
        if not isinstance(filename, str) or not isinstance(delimeter, str):
            raise Exception("filename and delimeter must be string types")
        

if __name__ == "__main__":
    logging.basicConfig(format="[%(filename)s:%(lineno)d]:%(levelname)s: %(message)s", level=logging.INFO)
    yt = ytmp3()
    
    logging.info("Please input the name(s) of song(s) to download")
    inp = input()
    while inp != "exit":
        Thread(target = yt.search_and_download, args = (inp, lambda res: 0)).start()
        inp = input()