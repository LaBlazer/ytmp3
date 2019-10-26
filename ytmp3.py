import logging
import requests
import sys
import inspect
from os import path
from threading import Thread
from youtube_dl import YoutubeDL
from youtube_api import YoutubeDataApi

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

    def __init__(self, api_key):
        self.log = logging.getLogger("ytmp3")
        ytmp3.options["logger"] = self.log
        self.api_key = api_key
        self.api = YoutubeDataApi(api_key)
        self.ytd = YoutubeDL(ytmp3.options)

    def _load_file(self, filename):
        pass

    def search(self, query, max_results = 6):
        if not isinstance(query, str):
            raise Exception("query must be a string type")

        results = []
        try:
            for v in self.api.search(query, max_results=max_results):
                vid = {}
                vid['title'] = v['video_title']
                vid['author'] = v['channel_title']
                vid['id'] = v["video_id"]
                vid['url'] = v["video_id"]
                vid['date'] = v['video_publish_date']
                vid['thumb'] = v['video_thumbnail']
                results.append(vid)

                self.log.debug(f"Title: {v['video_title']}, Url: {v['video_id']}, Date: {v['video_publish_date']}, \
                Author:{v['channel_title']}, Thumb: {v['video_thumbnail']}")

        except Exception as ex:
            self.log.error(f"Error while scraping youtube: {ex}")

        return results

    def download(self, video_ids):
        if not isinstance(next(iter(video_ids), None), str):
            raise Exception("video ids must be a list of strings type")
        
        self.ytd.download(video_ids)

    def search_and_download(self, query, callback, max_results = 6):
        if not callable(callback):
            raise Exception("callback must be a callable object")
        
        results = self.search(query, max_results)

        index = 0
        if len(results) > 0:
            index = callback(results)

        if index >= 0 and index < len(results):
            self.log.info(f"Downloading '{results[index].get('title')}'")
            self.download([results[index].get('id')])
        else:
            raise Exception("callback returned invalid index")
        self.log.info(f"Done")
        
    def read_and_download(self, filename, delimeter = '\n'):
        if not isinstance(filename, str) or not isinstance(delimeter, str):
            raise Exception("filename and delimeter must be string types")
        

if __name__ == "__main__":
    logging.basicConfig(format="[%(filename)s:%(lineno)d]:%(levelname)s: %(message)s", level=logging.INFO)
    yt = ytmp3()
    
    inp = ""
    while inp != "exit":
        inp = input("Search query: ")
        Thread(target = yt.search_and_download, args = (inp, lambda res: 0, 1)).start()