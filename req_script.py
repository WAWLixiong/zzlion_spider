from mitmproxy import ctx
# import json
import hashlib
# import requests
import wget

def request(flow):
    request=flow.request
    RUS=request.url.startswith
    if RUS('http://v6-dy.ixigua.com') or RUS('http://v1-dy.ixigua.com') or RUS('http://v3-dy.ixigua.com') or RUS('http://v9-dy.ixigua.com'):
        with open('D:\\video_url.txt','a') as f:
            f.write(request.url+'\n')
        # resp=requests.get(request.url).content
        url_hash=hashlib.md5(request.url.encode('utf-8')).hexdigest()
        # with open('D:\\douyin_video\\{name}.mp4'.format(name=url_hash),'wb') as f:
        # 	f.write(resp)
        wget.download(url=request.url,out='D:\\douyin_video\\{name}.mp4'.format(name=url_hash))